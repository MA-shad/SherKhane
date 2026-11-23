import { useState, useEffect, useRef } from "react";
import { Link } from "react-router";

export function meta() {
  return [
    { title: "مشاعره هوشمند با هوش مصنوعی | شعرخانه" },
    {
      name: "description",
      content: "در مسابقه مشاعره آنلاین با گنجینه ادب فارسی و ربات هوشمند شعرخانه به رقابت بپردازید و تسلط ادبی خود را بسنجید.",
    },
    { property: "og:title", content: "مشاعره هوشمند شعرخانه" },
    { property: "og:description", content: "بازی آنلاین مشاعره با هوش مصنوعی شعرخانه بر پایه دیوان کهن فارسی." },
  ];
}

const TURN_TIME_LIMIT = 45; // ۴۵ ثانیه مهلت برای هر نوبت

export default function MoshaerehPage() {
  const [gameState, setGameState] = useState("idle"); // idle | playing | game_over
  const [session, setSession] = useState(null);
  const [turns, setTurns] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [timeLeft, setTimeLeft] = useState(TURN_TIME_LIMIT);

  const turnsEndRef = useRef(null);
  const inputRef = useRef(null);

  // اسکرول نرم به آخرین بیت ارسال‌شده
  useEffect(() => {
    turnsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns]);

  // تمرکز روی کادر ورودی در شروع نوبت جدید
  useEffect(() => {
    if (gameState === "playing" && !isLoading) {
      inputRef.current?.focus();
    }
  }, [gameState, isLoading]);

  // تایمر معکوس برای نوبت کاربر
  useEffect(() => {
    if (gameState !== "playing" || isLoading) return;

    if (timeLeft <= 0) {
      handleTimeOut();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [gameState, isLoading, timeLeft]);

  // اتمام زمان نوبت کاربر
  const handleTimeOut = () => {
    setGameState("game_over");
    setFeedback({
      type: "error",
      message: "مهلت زمان شما به پایان رسید! این دور از مشاعره متوقف شد.",
    });
  };

  // شروع بازی جدید
  const handleStartGame = async () => {
    setIsLoading(true);
    setFeedback(null);
    setTurns([]);

    try {
      const response = await fetch("http://localhost:8000/api/games/moshaereh/start/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        throw new Error("خطا در ایجاد نشست جدید بازی.");
      }

      const data = await response.json();
      setSession(data);
      setGameState("playing");
      setTimeLeft(TURN_TIME_LIMIT);
      setTurns([
        {
          id: "welcome",
          sender: "system",
          text: `بازی آغاز شد! داور مسابقه برای دور اول، حرف «${data.current_letter}» را تعیین کرد. بیتی آغازین با این حرف بفرمایید:`,
          timestamp: new Date().toLocaleTimeString("fa-IR"),
        },
      ]);
    } catch (err) {
      setFeedback({
        type: "error",
        message: err.message || "امکان ارتباط با سرور وجود ندارد.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // ارسال نوبت کاربر
  const handleSubmitTurn = async (e) => {
    e?.preventDefault();
    const trimmed = inputText.trim();
    if (!trimmed || isLoading || !session) return;

    setIsLoading(true);
    setFeedback(null);

    // افزودن بیت کاربر به لیست گفتگو
    const userTurn = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: trimmed,
      timestamp: new Date().toLocaleTimeString("fa-IR"),
    };
    setTurns((prev) => [...prev, userTurn]);
    setInputText("");

    try {
      const response = await fetch(
        `http://localhost:8000/api/games/moshaereh/${session.id}/play/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ verse_text: trimmed }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        // خطای داوری (شعر اشتباه یا کوتاه یا حرف نامطابق)
        const errorText = data.message || data.detail || (data.verse_text ? data.verse_text[0] : "بیت ارسالی پذیرفته نشد.");
        setFeedback({ type: "error", message: errorText });
        return;
      }

      // به‌روزرسانی اطلاعات سشن (امتیاز و حرف جاری)
      if (data.session) {
        setSession(data.session);
        if (!data.session.is_active) {
          setGameState("game_over");
        }
      }

      // ثبت پاسخ ربات
      if (data.bot_verse) {
        const botCouplet = `${data.bot_verse.first_couplet} / ${data.bot_verse.second_couplet}`;
        const botTurn = {
          id: `bot-${Date.now()}`,
          sender: "bot",
          text: botCouplet,
          poet: data.bot_verse.poem?.poet?.name || "شاعر کهن",
          poemTitle: data.bot_verse.poem?.title,
          timestamp: new Date().toLocaleTimeString("fa-IR"),
        };
        setTurns((prev) => [...prev, botTurn]);
      }

      // اگر کاربر برنده شده باشد
      if (!data.session.is_active && !data.bot_verse) {
        setFeedback({
          type: "success",
          message: data.message || "آفرین! شما برنده مسابقه مشاعره شدید!",
        });
      } else {
        setFeedback({
          type: "success",
          message: `بیت شما تایید شد (+۱۰ امتیاز). نوبت بعدی با حرف «${data.session.current_letter}» است.`,
        });
        setTimeLeft(TURN_TIME_LIMIT); // ریست شدن تایمر برای نوبت بعدی
      }
    } catch (err) {
      setFeedback({
        type: "error",
        message: "خطا در برقراری ارتباط با وب‌سرویس بازی.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // درصد پیشرفت تایمر
  const timerPercentage = Math.max(0, Math.min(100, (timeLeft / TURN_TIME_LIMIT) * 100));
  const timerColor =
    timeLeft > 20
      ? "bg-amber-600"
      : timeLeft > 10
      ? "bg-orange-600"
      : "bg-red-600 animate-pulse";

  return (
    <div className="py-6 max-w-4xl mx-auto space-y-8">
      {/* هدر بالایی صفحه */}
      <div className="rounded-xl p-8 bg-[#29322c] text-[#f7f1e5] relative overflow-hidden shadow-xl border border-amber-900/30">
        <div className="absolute -left-12 -top-12 w-64 h-64 rounded-full border border-amber-400/10 pointer-events-none" />
        <div className="relative z-10 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/15 text-amber-300 text-xs font-semibold tracking-wide border border-amber-500/20">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
            میدان مشاعره شعرخانه
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-[#f6f3ec]">
            مشاعره با هوش مصنوعی و گنجینه دیوان
          </h1>
          <p className="text-sm text-zinc-300 max-w-2xl leading-relaxed">
            با داوری دقیق قواعد عروضی، حرف آخر هر بیت چالش دور بعد است. دانش ادبی و حافظه شعری خود را در مصاف با حافظ، سعدی و خیام محک بزنید.
          </p>
        </div>
      </div>

      {/* وضعیت لابی / قبل از شروع بازی */}
      {gameState === "idle" && (
        <div className="bg-[#eee9dd] border border-[#d6cebe] rounded-xl p-10 text-center space-y-6 shadow-sm">
          <div className="w-20 h-20 mx-auto rounded-full bg-[#29322c] text-amber-300 flex items-center justify-center text-3xl font-extrabold shadow-inner border border-amber-600/30">
            مش
          </div>
          <div className="space-y-2 max-w-lg mx-auto">
            <h2 className="text-xl font-bold text-[#252b27]">آماده رقابت هستید؟</h2>
            <p className="text-sm text-zinc-600 leading-relaxed">
              با آغاز بازی، داور سامانه یک حرف تصادفی را برمی‌گزیند. برای هر نوبت ۴۵ ثانیه مهلت دارید بیتی خوش‌آهنگ بسرایید یا از یاد برخوانید.
            </p>
          </div>
          <button
            onClick={handleStartGame}
            disabled={isLoading}
            className="inline-flex items-center justify-center gap-2 px-8 py-3.5 bg-[#29322c] hover:bg-[#1f2621] text-amber-300 font-bold text-base rounded-lg transition-all shadow-md hover:shadow-lg hover:scale-105 active:scale-95 disabled:opacity-50 cursor-pointer"
          >
            {isLoading ? "در حال آماده‌سازی مسابقه..." : "آغاز مسابقه مشاعره"}
            <span aria-hidden="true">←</span>
          </button>
        </div>
      )}

      {/* محوطه مسابقه و بازی فعال یا پایان‌یافته */}
      {gameState !== "idle" && (
        <div className="space-y-6">
          {/* پنل شاخص‌های زنده (داشبورد مسابقه) */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* حرف جاری */}
            <div className="bg-[#eee9dd] border border-[#d6cebe] rounded-xl p-4 text-center shadow-sm">
              <span className="text-xs text-zinc-500 font-medium block mb-1">حرف هدف دور</span>
              <span className="text-3xl font-extrabold text-amber-800 drop-shadow-sm">
                «{session?.current_letter || "—"}»
              </span>
            </div>

            {/* امتیاز مسابقه */}
            <div className="bg-[#eee9dd] border border-[#d6cebe] rounded-xl p-4 text-center shadow-sm">
              <span className="text-xs text-zinc-500 font-medium block mb-1">امتیاز شما</span>
              <span className="text-3xl font-extrabold text-emerald-800">
                {session?.score ?? 0}
              </span>
            </div>

            {/* تعداد دورها */}
            <div className="bg-[#eee9dd] border border-[#d6cebe] rounded-xl p-4 text-center shadow-sm">
              <span className="text-xs text-zinc-500 font-medium block mb-1">دور مسابقه</span>
              <span className="text-3xl font-extrabold text-zinc-800">
                {session?.round_count ?? 0}
              </span>
            </div>

            {/* مهلت زمان */}
            <div className="bg-[#eee9dd] border border-[#d6cebe] rounded-xl p-4 text-center shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs text-zinc-500 font-medium block mb-1">زمان باقیمانده</span>
                <span className={`text-2xl font-black ${timeLeft <= 10 ? "text-red-700 animate-pulse" : "text-zinc-800"}`}>
                  {timeLeft} ثانیه
                </span>
              </div>
              <div className="w-full bg-zinc-300 h-1.5 rounded-full overflow-hidden mt-2">
                <div
                  className={`h-full transition-all duration-1000 ${timerColor}`}
                  style={{ width: `${timerPercentage}%` }}
                />
              </div>
            </div>
          </div>

          {/* میدان نبرد و زنجیره ابیات خوانده‌شده */}
          <div className="bg-[#fbf9f4] border border-[#e1d9ca] rounded-2xl p-6 min-h-[380px] max-h-[520px] overflow-y-auto space-y-4 shadow-inner">
            {turns.map((turn) => {
              if (turn.sender === "system") {
                return (
                  <div
                    key={turn.id}
                    className="p-3.5 bg-amber-500/10 border border-amber-600/25 rounded-lg text-amber-950 text-xs md:text-sm text-center font-medium"
                  >
                    {turn.text}
                  </div>
                );
              }

              const isUser = turn.sender === "user";
              return (
                <div
                  key={turn.id}
                  className={`flex flex-col ${isUser ? "items-end" : "items-start"} space-y-1`}
                >
                  <div className="flex items-center gap-2 px-1 text-xs text-zinc-500">
                    <span>{isUser ? "بیت شما" : "پاسخ ربات شعرخانه"}</span>
                    <span>•</span>
                    <span>{turn.timestamp}</span>
                  </div>

                  <div
                    className={`max-w-xl p-4 rounded-2xl shadow-sm text-sm md:text-base leading-loose ${
                      isUser
                        ? "bg-[#29322c] text-[#f6f3ec] rounded-br-none border border-zinc-700"
                        : "bg-[#eee9dd] text-[#252b27] rounded-bl-none border border-[#d3c9b7]"
                    }`}
                  >
                    <p className="font-semibold">{turn.text}</p>
                    {turn.poet && (
                      <div className="mt-2 pt-2 border-t border-zinc-400/30 text-xs text-amber-800 flex items-center justify-between">
                        <span>شاعر: {turn.poet}</span>
                        {turn.poemTitle && <span>({turn.poemTitle})</span>}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
            <div ref={turnsEndRef} />
          </div>

          {/* نوار بازخورد و اخطارهای داور */}
          {feedback && (
            <div
              className={`p-3.5 rounded-lg text-xs md:text-sm font-medium border flex items-center justify-between transition-all ${
                feedback.type === "error"
                  ? "bg-red-50 text-red-900 border-red-200"
                  : "bg-emerald-50 text-emerald-900 border-emerald-200"
              }`}
            >
              <span>{feedback.message}</span>
              <button
                onClick={() => setFeedback(null)}
                className="text-xs opacity-70 hover:opacity-100 cursor-pointer"
              >
                ✕
              </button>
            </div>
          )}

          {/* کادر ارسال شعر یا دکمه بازی دوباره */}
          {gameState === "playing" ? (
            <form onSubmit={handleSubmitTurn} className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={`بیت خود را با حرف «${session?.current_letter}» بنویسید...`}
                disabled={isLoading}
                className="flex-1 px-4 py-3.5 rounded-xl border border-[#c4baaa] bg-[#fbf9f4] text-[#252b27] placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-amber-600/40 focus:border-amber-700 text-sm md:text-base"
              />
              <button
                type="submit"
                disabled={isLoading || !inputText.trim()}
                className="px-6 py-3.5 bg-[#29322c] hover:bg-[#1f2621] text-amber-300 font-bold rounded-xl transition-all shadow disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer flex items-center gap-2"
              >
                {isLoading ? "داوری..." : "ارسال بیت"}
              </button>
            </form>
          ) : (
            <div className="p-6 bg-[#eee9dd] border border-[#d6cebe] rounded-xl text-center space-y-4">
              <p className="font-bold text-[#252b27] text-lg">
                مسابقه پایان یافت! امتیاز نهایی شما: {session?.score ?? 0}
              </p>
              <button
                onClick={handleStartGame}
                disabled={isLoading}
                className="px-8 py-3 bg-[#29322c] hover:bg-[#1f2621] text-amber-300 font-bold rounded-lg transition-all shadow cursor-pointer"
              >
                شروع یک مسابقه تازه
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
