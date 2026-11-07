/**
 * SherKhaneh Main Application Controller
 * High-performance, responsive Persian UI controller with clean view routing,
 * live interactive games, Mushaereh engine, and Memorization studio.
 */

// Application State
const State = {
  activeView: 'home',
  theme: localStorage.getItem('sherkhaneh_theme') || 'light',
  user: {
    username: 'کاربر مهمان',
    display_name: 'ادیب دوستدار شعر',
    xp: parseInt(localStorage.getItem('sherkhaneh_xp') || '150'),
    streak: parseInt(localStorage.getItem('sherkhaneh_streak') || '3'),
    title: 'حافظ‌یار'
  },
  currentPoem: null,
  activePoemsList: [],
  selectedPoetFilter: 'all',
  bookmarks: JSON.parse(localStorage.getItem('sherkhaneh_bookmarks') || '[]'),
  mushaereh: {
    room_id: null,
    current_letter: 'م',
    score_user: 0,
    score_bot: 0,
    timer: 45,
    timerInterval: null,
    turns: []
  },
  game: {
    currentScore: 0
  }
};

// DOM Ready initialization
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  setupNavigation();
  loadDailyContent();
  loadTreasury();
  setupMushaereh();
  setupGames();
  setupMemorization();
  updateUserUI();
});

// Toast Notifications
function showToast(message) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// Theme Toggle
function initTheme() {
  document.documentElement.setAttribute('data-theme', State.theme);
  const themeBtn = document.getElementById('btn-toggle-theme');
  if (themeBtn) {
    themeBtn.innerHTML = State.theme === 'dark' ? '☀️' : '🌙';
    themeBtn.addEventListener('click', () => {
      State.theme = State.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', State.theme);
      localStorage.setItem('sherkhaneh_theme', State.theme);
      themeBtn.innerHTML = State.theme === 'dark' ? '☀️' : '🌙';
    });
  }
}

// Navigation between views
function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item, [data-navigate]');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      const targetView = item.getAttribute('data-view') || item.getAttribute('data-navigate');
      if (targetView) {
        switchView(targetView);
      }
    });
  });
}

function switchView(viewName) {
  State.activeView = viewName;
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-view') === viewName);
  });

  const activeSec = document.getElementById(`view-${viewName}`);
  if (activeSec) {
    activeSec.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  if (viewName === 'notebook') renderNotebook();
  if (viewName === 'profile') renderProfile();
}

function updateUserUI() {
  const xpEl = document.getElementById('user-xp-display');
  const streakEl = document.getElementById('user-streak-display');
  const titleEl = document.getElementById('user-title-display');

  if (xpEl) xpEl.textContent = `${State.user.xp} XP`;
  if (streakEl) streakEl.textContent = `${State.user.streak} روز`;
  if (titleEl) titleEl.textContent = State.user.title;
}

function addXP(amount) {
  State.user.xp += amount;
  localStorage.setItem('sherkhaneh_xp', State.user.xp.toString());
  updateUserUI();
}

// -------------------------------------------------------------
// 1. Home & Daily Content
// -------------------------------------------------------------
async function loadDailyContent() {
  try {
    const data = await ApiClient.request('/daily/culture/today/');
    if (data && data.beyt_of_day) {
      document.getElementById('beyt-first').textContent = data.beyt_of_day.first_couplet;
      document.getElementById('beyt-second').textContent = data.beyt_of_day.second_couplet;
      document.getElementById('beyt-poet').textContent = `— ${data.beyt_of_day.poet}`;
      document.getElementById('beyt-commentary').textContent = data.beyt_of_day.commentary;
    }
    if (data && data.proverb_of_day) {
      document.getElementById('proverb-text').textContent = data.proverb_of_day.proverb;
      document.getElementById('proverb-meaning').textContent = data.proverb_of_day.meaning;
    }
  } catch (err) {
    console.error('Error loading daily content', err);
  }

  // Fal-e Hafez trigger
  const falBtn = document.getElementById('btn-draw-fal');
  if (falBtn) {
    falBtn.addEventListener('click', async () => {
      falBtn.disabled = true;
      falBtn.textContent = 'در حال تفأل به لسان‌الغیب...';
      const resultBox = document.getElementById('fal-result-box');
      resultBox.style.display = 'none';

      try {
        const fal = await ApiClient.request('/daily/culture/fal_hafez/');
        if (fal) {
          const versesContainer = document.getElementById('fal-verses');
          versesContainer.innerHTML = '';
          (fal.verses || []).slice(0, 3).forEach(v => {
            const p = document.createElement('p');
            p.textContent = `${v.first}  /  ${v.second}`;
            versesContainer.appendChild(p);
          });
          document.getElementById('fal-tafsir-text').textContent = fal.tafsir;
          resultBox.style.display = 'block';
          addXP(10);
        }
      } catch (err) {
        showToast('خطا در دریافت فال حافظ');
      } finally {
        falBtn.disabled = false;
        falBtn.textContent = 'نیت کنید و تفأل زنید';
      }
    });
  }
}

// -------------------------------------------------------------
// 2. Poetry Treasury (گنجینه ادب)
// -------------------------------------------------------------
async function loadTreasury() {
  const poetsChipsContainer = document.getElementById('poet-filter-chips');
  const poemsGrid = document.getElementById('treasury-poems-grid');
  const searchInput = document.getElementById('poetry-search-input');

  // Load poets
  try {
    const poetsData = await ApiClient.request('/poetry/poets/');
    const poets = poetsData.results || [];
    poets.forEach(poet => {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = poet.name;
      chip.dataset.poetSlug = poet.slug;
      chip.addEventListener('click', () => {
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        State.selectedPoetFilter = poet.slug;
        filterAndRenderPoems();
      });
      poetsChipsContainer.appendChild(chip);
    });
  } catch (e) {}

  // Load poems
  try {
    const poemsData = await ApiClient.request('/poetry/poems/');
    State.activePoemsList = poemsData.results || [];
    renderPoemsGrid(State.activePoemsList);
  } catch (e) {}

  // Search event
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      const filtered = State.activePoemsList.filter(p => 
        p.title.toLowerCase().includes(q) ||
        (p.poet_name && p.poet_name.toLowerCase().includes(q)) ||
        (p.first_verse && p.first_verse.toLowerCase().includes(q))
      );
      renderPoemsGrid(filtered);
    });
  }

  // All poets chip
  const chipAll = document.getElementById('chip-all-poets');
  if (chipAll) {
    chipAll.addEventListener('click', () => {
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chipAll.classList.add('active');
      State.selectedPoetFilter = 'all';
      filterAndRenderPoems();
    });
  }
}

function filterAndRenderPoems() {
  let list = State.activePoemsList;
  if (State.selectedPoetFilter !== 'all') {
    list = list.filter(p => p.poet && p.poet.slug === State.selectedPoetFilter);
  }
  renderPoemsGrid(list);
}

function renderPoemsGrid(poems) {
  const grid = document.getElementById('treasury-poems-grid');
  if (!grid) return;
  grid.innerHTML = '';

  if (poems.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--color-ink-muted);">هیچ شعری با این مشخصات یافت نشد.</div>';
    return;
  }

  poems.forEach(poem => {
    const card = document.createElement('div');
    card.className = 'poem-card';
    card.innerHTML = `
      <div>
        <div class="poem-header">
          <span class="poet-pill">${poem.poet ? poem.poet.name : (poem.poet_name || 'شاعر پارسی')}</span>
          <span style="font-size: 0.75rem; color: var(--color-ink-muted);">${poem.poem_type || 'غزل'}</span>
        </div>
        <h3 class="poem-title">${poem.title}</h3>
        <p class="poem-matla">${poem.first_verse || (poem.verses && poem.verses[0] ? `${poem.verses[0].first_couplet} / ${poem.verses[0].second_couplet}` : '...')}</p>
      </div>
      <div class="poem-footer">
        <span>وزن: ${poem.rhythm_name || (poem.rhythm ? poem.rhythm.name : 'عروضی')}</span>
        <span style="color: var(--color-gold-accent); font-weight: 600;">خوانش ◀</span>
      </div>
    `;
    card.addEventListener('click', () => openPoemReader(poem));
    grid.appendChild(card);
  });
}

// -------------------------------------------------------------
// 3. Poem Reader View (خوانشگر اختصاصی)
// -------------------------------------------------------------
function openPoemReader(poem) {
  State.currentPoem = poem;
  const modal = document.getElementById('poem-reader-modal');
  document.getElementById('reader-title').textContent = poem.title;
  document.getElementById('reader-poet').textContent = poem.poet ? poem.poet.name : (poem.poet_name || '');
  document.getElementById('reader-rhythm').textContent = poem.rhythm ? poem.rhythm.name : (poem.rhythm_name || '');
  document.getElementById('reader-edition').textContent = poem.edition_source || 'نسخه مصحح مرجع';

  const body = document.getElementById('reader-verses-container');
  body.innerHTML = '';

  const verses = poem.verses || [];
  verses.forEach(v => {
    const row = document.createElement('div');
    row.className = 'verse-row';
    row.innerHTML = `
      <div class="couplet-first">${v.first_couplet}</div>
      <div class="couplet-second">${v.second_couplet}</div>
    `;
    row.title = 'کلیک برای کپی کردن بیت';
    row.addEventListener('click', () => {
      const text = `${v.first_couplet} / ${v.second_couplet} (${poem.poet ? poem.poet.name : ''})`;
      navigator.clipboard.writeText(text);
      showToast('بیت با موفقیت کپی شد.');
    });
    body.appendChild(row);
  });

  // Bookmark toggle
  const bmBtn = document.getElementById('btn-toggle-bookmark');
  const isBookmarked = State.bookmarks.some(b => b.id === poem.id);
  bmBtn.textContent = isBookmarked ? '★ در دفترچه' : '☆ افزودن به دفترچه';
  bmBtn.onclick = () => {
    toggleBookmark(poem);
    const updated = State.bookmarks.some(b => b.id === poem.id);
    bmBtn.textContent = updated ? '★ در دفترچه' : '☆ افزودن به دفترچه';
  };

  // Memorize button
  const memBtn = document.getElementById('btn-memorize-this');
  memBtn.onclick = () => {
    closePoemReader();
    switchView('memorization');
    startMemorizationPractice(poem);
  };

  modal.classList.add('active');
}

function closePoemReader() {
  const modal = document.getElementById('poem-reader-modal');
  if (modal) modal.classList.remove('active');
}

document.getElementById('btn-close-reader').addEventListener('click', closePoemReader);

// -------------------------------------------------------------
// 4. Personal Notebook (دفترچه شخصی)
// -------------------------------------------------------------
function toggleBookmark(poem) {
  const idx = State.bookmarks.findIndex(b => b.id === poem.id);
  if (idx > -1) {
    State.bookmarks.splice(idx, 1);
    showToast('شعر از دفترچه شخصی حذف شد.');
  } else {
    State.bookmarks.push({
      id: poem.id,
      title: poem.title,
      poet_name: poem.poet ? poem.poet.name : poem.poet_name,
      first_verse: poem.first_verse || (poem.verses && poem.verses[0] ? poem.verses[0].first_couplet : ''),
      added_at: new Date().toLocaleDateString('fa-IR')
    });
    addXP(15);
    showToast('شعر به دفترچه شخصی اضافه شد.');
  }
  localStorage.setItem('sherkhaneh_bookmarks', JSON.stringify(State.bookmarks));
}

function renderNotebook() {
  const container = document.getElementById('notebook-items-grid');
  if (!container) return;
  container.innerHTML = '';

  if (State.bookmarks.length === 0) {
    container.innerHTML = '<div style="text-align:center; padding: 48px; color: var(--color-ink-muted);">دفترچه شما هنوز خالی است. اشعار دلخواه را از گنجینه نشانه‌گذاری کنید.</div>';
    return;
  }

  State.bookmarks.forEach(bm => {
    const card = document.createElement('div');
    card.className = 'poem-card';
    card.innerHTML = `
      <div class="poem-header">
        <span class="poet-pill">${bm.poet_name}</span>
        <span style="font-size: 0.75rem; color: var(--color-ink-muted);">${bm.added_at}</span>
      </div>
      <h3 class="poem-title">${bm.title}</h3>
      <p class="poem-matla">${bm.first_verse}</p>
      <div class="poem-footer">
        <span style="color: var(--color-ruby-poetic); cursor: pointer;" class="btn-remove-bm">حذف نشان</span>
        <span style="color: var(--color-gold-accent); font-weight: 600;">بازخوانی ◀</span>
      </div>
    `;
    card.querySelector('.btn-remove-bm').addEventListener('click', (e) => {
      e.stopPropagation();
      toggleBookmark(bm);
      renderNotebook();
    });
    card.addEventListener('click', () => {
      const fullPoem = State.activePoemsList.find(p => p.id === bm.id);
      if (fullPoem) openPoemReader(fullPoem);
    });
    container.appendChild(card);
  });
}

// -------------------------------------------------------------
// 5. Mushaereh Arena (میدان مشاعره زنده)
// -------------------------------------------------------------
function setupMushaereh() {
  const startBtn = document.getElementById('btn-start-mushaereh');
  const sendBtn = document.getElementById('btn-send-verse');
  const inputEl = document.getElementById('mushaereh-verse-input');

  if (startBtn) {
    startBtn.addEventListener('click', () => startNewMushaereh());
  }

  if (sendBtn && inputEl) {
    sendBtn.addEventListener('click', () => submitMushaerehVerse());
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') submitMushaerehVerse();
    });
  }
}

function startNewMushaereh() {
  State.mushaereh.turns = [];
  State.mushaereh.score_user = 0;
  State.mushaereh.score_bot = 0;
  const initialLetters = ['م', 'ن', 'د', 'ر', 'ی', 'ب', 'ت', 'س', 'ک', 'ش'];
  State.mushaereh.current_letter = initialLetters[Math.floor(Math.random() * initialLetters.length)];

  document.getElementById('arena-current-letter').textContent = State.mushaereh.current_letter;
  document.getElementById('arena-user-score').textContent = '۰';
  document.getElementById('arena-bot-score').textContent = '۰';
  document.getElementById('mushaereh-log').innerHTML = '';

  addTurnBubble('system', `مسابقه آغاز شد! نوبت شماست. بیتی بخوانید که با حرف «${State.mushaereh.current_letter}» آغاز شود.`);
  resetMushaerehTimer();
}

function resetMushaerehTimer() {
  clearInterval(State.mushaereh.timerInterval);
  State.mushaereh.timer = 45;
  const timerEl = document.getElementById('mushaereh-timer-display');
  if (timerEl) timerEl.textContent = `${State.mushaereh.timer} ثانیه`;

  State.mushaereh.timerInterval = setInterval(() => {
    State.mushaereh.timer--;
    if (timerEl) timerEl.textContent = `${State.mushaereh.timer} ثانیه`;
    if (State.mushaereh.timer <= 0) {
      clearInterval(State.mushaereh.timerInterval);
      addTurnBubble('system', 'مهلت زمانی شما به پایان رسید! امتیاز این دور به حریف رسید.');
    }
  }, 1000);
}

function submitMushaerehVerse() {
  const inputEl = document.getElementById('mushaereh-verse-input');
  const verseText = inputEl.value.trim();
  if (!verseText) return;

  // Real-time client & server validation
  const firstChar = verseText.replace(/[\s\.\،«»]/g, '')[0];
  if (!firstChar || firstChar !== State.mushaereh.current_letter) {
    showToast(`بیت باید با حرف «${State.mushaereh.current_letter}» آغاز شود!`);
    return;
  }

  // Check duplicate
  if (State.mushaereh.turns.some(t => t.text === verseText)) {
    showToast('این بیت قبلاً در مسابقه خوانده شده است!');
    return;
  }

  inputEl.value = '';
  State.mushaereh.score_user += 10;
  document.getElementById('arena-user-score').textContent = State.mushaereh.score_user.toString();
  addXP(10);

  // Extract ending letter
  const cleaned = verseText.replace(/[\s\.\،\؛\!\؟«»]/g, '');
  const endChar = cleaned[cleaned.length - 1];

  addTurnBubble('user', verseText);
  State.mushaereh.turns.push({ sender: 'user', text: verseText });
  State.mushaereh.current_letter = endChar;
  document.getElementById('arena-current-letter').textContent = endChar;

  // Bot response with authentic verse
  setTimeout(() => botRespondMushaereh(endChar), 1200);
}

function botRespondMushaereh(targetLetter) {
  // Search pool of verses
  const pool = [];
  FALLBACK_POETRY_STORE.poems.forEach(p => {
    p.verses.forEach(v => {
      const full = `${v.first_couplet} / ${v.second_couplet}`;
      const fChar = v.first_couplet.replace(/[\s\.\،«»]/g, '')[0];
      if (fChar === targetLetter && !State.mushaereh.turns.some(t => t.text === full)) {
        pool.push({ verse: full, poet: p.poet.name });
      }
    });
  });

  if (pool.length === 0) {
    addTurnBubble('system', 'سخن‌سنج بیتی نیافت! شما پیروز این مسابقه شدید! 🏆');
    addXP(50);
    clearInterval(State.mushaereh.timerInterval);
    return;
  }

  const chosen = pool[Math.floor(Math.random() * pool.length)];
  State.mushaereh.score_bot += 10;
  document.getElementById('arena-bot-score').textContent = State.mushaereh.score_bot.toString();

  addTurnBubble('bot', chosen.verse, chosen.poet);
  State.mushaereh.turns.push({ sender: 'bot', text: chosen.verse });

  const cleaned = chosen.verse.replace(/[\s\.\،\؛\!\؟«»]/g, '');
  const nextLetter = cleaned[cleaned.length - 1];
  State.mushaereh.current_letter = nextLetter;
  document.getElementById('arena-current-letter').textContent = nextLetter;

  resetMushaerehTimer();
}

function addTurnBubble(sender, text, poetName = '') {
  const container = document.getElementById('mushaereh-log');
  if (!container) return;
  const bubble = document.createElement('div');
  bubble.className = `turn-bubble ${sender}`;

  if (sender === 'system') {
    bubble.style.background = 'var(--color-surface-card)';
    bubble.style.border = '1px dashed var(--color-gold-gentle)';
    bubble.style.alignSelf = 'center';
    bubble.style.color = 'var(--color-gold-accent)';
    bubble.style.fontWeight = 'bold';
    bubble.textContent = text;
  } else {
    bubble.innerHTML = `
      <div class="turn-verse">${text}</div>
      <div class="turn-meta">${sender === 'user' ? 'شما' : `سخن‌سنج (${poetName})`}</div>
    `;
  }

  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

// -------------------------------------------------------------
// 6. Literary Games (سرای بازی‌های ادبی)
// -------------------------------------------------------------
function setupGames() {
  document.getElementById('btn-play-guess-poet').addEventListener('click', playGuessPoetGame);
  document.getElementById('btn-play-bait-chin').addEventListener('click', playBaitChinGame);
  document.getElementById('btn-play-word-quiz').addEventListener('click', playWordQuizGame);
}

function playGuessPoetGame() {
  const arena = document.getElementById('active-game-arena');
  arena.innerHTML = '';

  const poem = FALLBACK_POETRY_STORE.poems[Math.floor(Math.random() * FALLBACK_POETRY_STORE.poems.length)];
  const verse = poem.verses[0];
  const correctPoet = poem.poet.name;

  const allPoets = ['حافظ شیرازی', 'سعدی شیرازی', 'مولانا جلال‌الدین بلخی', 'حکیم فردوسی', 'خیام نیشابوری', 'نظامی گنجوی'];
  const distractors = allPoets.filter(p => p !== correctPoet).slice(0, 3);
  const options = [correctPoet, ...distractors].sort(() => Math.random() - 0.5);

  arena.innerHTML = `
    <div style="background: var(--color-surface-card); border: 1px solid var(--color-gold-gentle); border-radius: var(--radius-md); padding: 24px; text-align: center;">
      <h3 style="margin-bottom: 16px;">این بیت سرودهٔ کدام شاعر بزرگ است؟</h3>
      <p class="poetry-font" style="font-size: 1.5rem; margin-bottom: 24px; color: var(--color-gold-accent);">
        «${verse.first_couplet} / ${verse.second_couplet}»
      </p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 500px; margin: 0 auto;">
        ${options.map(opt => `<button class="chip btn-game-opt" style="padding: 14px; font-size: 1rem;">${opt}</button>`).join('')}
      </div>
      <div id="game-feedback" style="margin-top: 16px; font-weight: bold;"></div>
    </div>
  `;

  arena.querySelectorAll('.btn-game-opt').forEach(btn => {
    btn.addEventListener('click', () => {
      const fb = document.getElementById('game-feedback');
      if (btn.textContent === correctPoet) {
        fb.innerHTML = '<span style="color: var(--color-emerald-success);">آفرین! پاسخ کاملاً درست است. (+20 XP)</span>';
        addXP(20);
        setTimeout(playGuessPoetGame, 1800);
      } else {
        fb.innerHTML = `<span style="color: var(--color-ruby-poetic);">نادرست بود! پاسخ درست «${correctPoet}» است.</span>`;
      }
    });
  });
}

function playBaitChinGame() {
  const arena = document.getElementById('active-game-arena');
  const poem = FALLBACK_POETRY_STORE.poems[Math.floor(Math.random() * FALLBACK_POETRY_STORE.poems.length)];
  const originalVerses = [...poem.verses];
  const shuffled = [...poem.verses].sort(() => Math.random() - 0.5);

  arena.innerHTML = `
    <div style="background: var(--color-surface-card); border: 1px solid var(--color-gold-gentle); border-radius: var(--radius-md); padding: 24px;">
      <h3 style="margin-bottom: 8px;">بیت‌چین: ابیات زیر از «${poem.title}» را به ترتیب درست بچینید</h3>
      <p style="color: var(--color-ink-muted); margin-bottom: 16px;">روی هر بیت کلیک کنید تا به جایگاه بعدی اضافه شود:</p>
      <div id="bait-chin-pool" style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 24px;">
        ${shuffled.map(v => `<div class="chip bait-item" data-id="${v.id}" style="padding: 12px; text-align: center; font-size: 1.1rem; font-family: var(--font-poetry);">${v.first_couplet} / ${v.second_couplet}</div>`).join('')}
      </div>
      <h4>ترتیب انتخاب‌شده شما:</h4>
      <div id="bait-chin-selected" style="min-height: 80px; border: 2px dashed var(--color-gold-gentle); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 16px;"></div>
      <button id="btn-check-baitchin" class="fal-btn" style="width: 100%;">بررسی چینش ابیات</button>
      <div id="bait-chin-feedback" style="margin-top: 16px; text-align: center; font-weight: bold;"></div>
    </div>
  `;

  const selectedIds = [];
  arena.querySelectorAll('.bait-item').forEach(item => {
    item.addEventListener('click', () => {
      const id = parseInt(item.dataset.id);
      if (!selectedIds.includes(id)) {
        selectedIds.push(id);
        item.style.opacity = '0.4';
        item.style.pointerEvents = 'none';
        const p = document.createElement('p');
        p.className = 'poetry-font';
        p.style.fontSize = '1.1rem';
        p.style.marginBottom = '6px';
        p.textContent = `${selectedIds.length}. ${item.textContent}`;
        document.getElementById('bait-chin-selected').appendChild(p);
      }
    });
  });

  document.getElementById('btn-check-baitchin').addEventListener('click', () => {
    const isCorrect = selectedIds.every((id, idx) => originalVerses[idx] && originalVerses[idx].id === id);
    const fb = document.getElementById('bait-chin-feedback');
    if (isCorrect && selectedIds.length === originalVerses.length) {
      fb.innerHTML = '<span style="color: var(--color-emerald-success);">شاهکار! ترتیب ابیات کاملاً صحیح است. (+35 XP)</span>';
      addXP(35);
    } else {
      fb.innerHTML = '<span style="color: var(--color-ruby-poetic);">ترتیب ابیات دقیق نبود. دوباره تلاش کنید.</span>';
    }
  });
}

function playWordQuizGame() {
  const arena = document.getElementById('active-game-arena');
  const words = [
    { word: 'میغ', meaning: 'ابر باران‌زا', opts: ['ابر باران‌زا', 'باد خزان', 'آفتاب داغ', 'باران تند'] },
    { word: 'خوالیگر', meaning: 'آشپز دربار', opts: ['آشپز دربار', 'فرمانده سواران', 'طبیب خردورز', 'خزانه‌دار'] },
    { word: 'سمن‌بر', meaning: 'زیباروی و سپیدتن', opts: ['زیباروی و سپیدتن', 'پهلوان شکست‌ناپذیر', 'سرکش و نامهربان', 'پیر خردمند'] }
  ];
  const q = words[Math.floor(Math.random() * words.length)];

  arena.innerHTML = `
    <div style="background: var(--color-surface-card); border: 1px solid var(--color-gold-gentle); border-radius: var(--radius-md); padding: 24px; text-align: center;">
      <h3 style="margin-bottom: 12px;">معنای واژه کهن «${q.word}» در ادب کهن چیست؟</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 500px; margin: 20px auto 0;">
        ${q.opts.map(opt => `<button class="chip btn-word-opt" style="padding: 14px; font-size: 1rem;">${opt}</button>`).join('')}
      </div>
      <div id="word-feedback" style="margin-top: 16px; font-weight: bold;"></div>
    </div>
  `;

  arena.querySelectorAll('.btn-word-opt').forEach(btn => {
    btn.addEventListener('click', () => {
      const fb = document.getElementById('word-feedback');
      if (btn.textContent === q.meaning) {
        fb.innerHTML = '<span style="color: var(--color-emerald-success);">درست است! واژه‌دان برجسته‌ای هستید. (+15 XP)</span>';
        addXP(15);
      } else {
        fb.innerHTML = `<span style="color: var(--color-ruby-poetic);">نادرست بود. معنی درست «${q.meaning}» است.</span>`;
      }
    });
  });
}

// -------------------------------------------------------------
// 7. Memorization Studio (استودیو حفظ شعر)
// -------------------------------------------------------------
function setupMemorization() {
  // Can be launched from reader or direct view
}

function startMemorizationPractice(poem) {
  const container = document.getElementById('memorization-practice-box');
  if (!container) return;
  container.innerHTML = '';

  const verses = poem.verses || [];
  if (verses.length === 0) return;

  container.innerHTML = `
    <div style="background: var(--color-surface-card); border: 1px solid var(--color-gold-gentle); border-radius: var(--radius-lg); padding: 28px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2>تمرین حفظ: «${poem.title}»</h2>
        <span class="hero-tag">روش تکرار با فاصله (SM-2)</span>
      </div>
      <p style="color: var(--color-ink-subtle); margin-bottom: 24px;">کلمات پنهان‌شده در ابیات را در ذهن خود بازیابی کنید یا بنویسید:</p>
      <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
        ${verses.map((v, i) => `
          <div style="background: var(--color-surface-alt); padding: 14px; border-radius: var(--radius-sm); border-right: 4px solid var(--color-gold-accent);">
            <p class="poetry-font" style="font-size: 1.25rem;">
              ${v.first_couplet}  /  ${v.second_couplet.split(' ').map((w, idx) => idx === 1 ? '____' : w).join(' ')}
            </p>
          </div>
        `).join('')}
      </div>
      <div style="text-align: center;">
        <h4 style="margin-bottom: 12px;">میزان تسلط خود را ارزیابی کنید:</h4>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <button class="chip" onclick="submitSm2Rating(1)" style="color: var(--color-ruby-poetic);">۱: دوباره (فراموش کردم)</button>
          <button class="chip" onclick="submitSm2Rating(3)" style="color: var(--color-amber-warning);">۳: خوب (با کمی مکث)</button>
          <button class="chip" onclick="submitSm2Rating(5)" style="color: var(--color-emerald-success); font-weight: bold;">۵: عالی (تسلط کامل)</button>
        </div>
      </div>
    </div>
  `;
}

function submitSm2Rating(grade) {
  if (grade >= 3) {
    showToast('تسلط شما ثبت شد. موعد مرور بعدی در روزهای آتی تنظیم گردید. (+25 XP)');
    addXP(25);
  } else {
    showToast('کارت به جعبه مرور روزانه بازگشت تا تثبیت شود.');
  }
}

// -------------------------------------------------------------
// 8. Profile View
// -------------------------------------------------------------
function renderProfile() {
  document.getElementById('profile-xp').textContent = `${State.user.xp} XP`;
  document.getElementById('profile-streak').textContent = `${State.user.streak} روز پیاپی`;
  document.getElementById('profile-title').textContent = State.user.title;
  document.getElementById('profile-bookmarks-count').textContent = State.bookmarks.length.toString();
}
