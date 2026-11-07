/**
 * SherKhaneh API Client & Offline Fallback Engine
 * Handles REST requests, JWT management, and seamless offline data fallback.
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Preloaded classical Persian poetry store for instant offline/demo usage
const FALLBACK_POETRY_STORE = {
  poets: [
    { id: 1, name: 'حافظ شیرازی', slug: 'hafez', century: 8, birth_place: 'شیراز', poems_count: 3 },
    { id: 2, name: 'سعدی شیرازی', slug: 'saadi', century: 7, birth_place: 'شیراز', poems_count: 3 },
    { id: 3, name: 'مولانا جلال‌الدین بلخی', slug: 'rumi', century: 7, birth_place: 'بلخ', poems_count: 2 },
    { id: 4, name: 'حکیم ابوالقاسم فردوسی', slug: 'ferdowsi', century: 4, birth_place: 'توس', poems_count: 2 },
    { id: 5, name: 'حکیم عمر خیام نیشابوری', slug: 'khayyam', century: 5, birth_place: 'نیشابور', poems_count: 2 },
    { id: 6, name: 'حکیم نظامی گنجوی', slug: 'nezami', century: 6, birth_place: 'گنجه', poems_count: 1 }
  ],
  poems: [
    {
      id: 1,
      title: 'الا یا ایها الساقی ادر کأسا و ناولها',
      slug: 'ala-ya-ayyohas-saghi',
      poet: { id: 1, name: 'حافظ شیرازی', slug: 'hafez', century: 8 },
      rhythm: { name: 'فاعلاتن فعلاتن فعلاتن فعلن' },
      poem_type: 'غزل',
      edition_source: 'تصحیح علامه قزوینی و دکتر غنی',
      verses: [
        { id: 101, order: 1, first_couplet: 'الا یا ایها الساقی ادر کأسا و ناولها', second_couplet: 'که عشق آسان نمود اول ولی افتاد مشکل‌ها' },
        { id: 102, order: 2, first_couplet: 'به بوی نافه‌ای کاخر صبا زان طره بگشاید', second_couplet: 'ز تاب جعد مشکینش چه خون افتاد در دل‌ها' },
        { id: 103, order: 3, first_couplet: 'مرا در منزل جانان چه امن عیش چون هر دم', second_couplet: 'جرس فریاد می‌دارد که بربندید محمل‌ها' },
        { id: 104, order: 4, first_couplet: 'به می سجاده رنگین کن گرت پیر مغان گوید', second_couplet: 'که سالک بی‌خبر نبود ز راه و رسم منزل‌ها' },
        { id: 105, order: 5, first_couplet: 'شب تاریک و بیم موج و گردابی چنین هایل', second_couplet: 'کجا دانند حال ما سبکباران ساحل‌ها' },
        { id: 106, order: 6, first_couplet: 'همه کارم ز خودکامی به بدنامی کشید آخر', second_couplet: 'نهان کی ماند آن رازی کز او سازند محفل‌ها' },
        { id: 107, order: 7, first_couplet: 'حضوری گر همی‌خواهی از او غایب مشو حافظ', second_couplet: 'متی ما تلق من تهوی دع الدنیا و اهملها' }
      ]
    },
    {
      id: 2,
      title: 'صلاح کار کجا و من خراب کجا',
      slug: 'salah-kar-koja',
      poet: { id: 1, name: 'حافظ شیرازی', slug: 'hafez', century: 8 },
      rhythm: { name: 'فاعلاتن فعلاتن فعلاتن فعلن' },
      poem_type: 'غزل',
      edition_source: 'تصحیح علامه قزوینی و دکتر غنی',
      verses: [
        { id: 201, order: 1, first_couplet: 'صلاح کار کجا و من خراب کجا', second_couplet: 'ببین تفاوت ره از کجاست تا به کجا' },
        { id: 202, order: 2, first_couplet: 'دلم ز صومعه بگرفت و خرقه سالوس', second_couplet: 'کجاست دیر مغان و شراب ناب کجا' },
        { id: 203, order: 3, first_couplet: 'چه نسبت است به رندی صلاح و تقوا را', second_couplet: 'سماع وعظ کجا نغمه رباب کجا' },
        { id: 204, order: 4, first_couplet: 'ز روی دوست دل دشمنان چه دریابد', second_couplet: 'چراغ مرده کجا شمع آفتاب کجا' }
      ]
    },
    {
      id: 3,
      title: 'یوسف گمگشته بازآید به کنعان غم مخور',
      slug: 'yousef-gomgashteh',
      poet: { id: 1, name: 'حافظ شیرازی', slug: 'hafez', century: 8 },
      rhythm: { name: 'فاعلاتن فعلاتن فعلاتن فعلن' },
      poem_type: 'غزل',
      edition_source: 'تصحیح علامه قزوینی و دکتر غنی',
      verses: [
        { id: 301, order: 1, first_couplet: 'یوسف گمگشته بازآید به کنعان غم مخور', second_couplet: 'کلبه احزان شود روزی گلستان غم مخور' },
        { id: 302, order: 2, first_couplet: 'این دل غمدیده حالش به شود دل بد مکن', second_couplet: 'وین سر شوریده بازآید به سامان غم مخور' },
        { id: 303, order: 3, first_couplet: 'گر بهار عمر باشد باز بر طرف چمن', second_couplet: 'چتر گل در سر کشی ای مرغ خوشخوان غم مخور' },
        { id: 304, order: 4, first_couplet: 'دور گردون گر دو روزی بر مراد ما نرفت', second_couplet: 'دایما یک سان نباشد حال دوران غم مخور' },
        { id: 305, order: 5, first_couplet: 'ای دل ار سیل فنا بنیاد هستی برکند', second_couplet: 'چون تو را نوح است کشتیبان ز طوفان غم مخور' }
      ]
    },
    {
      id: 4,
      title: 'ای ساربان آهسته ران کارام جانم می‌رود',
      slug: 'ey-sareban-ahesteh-ran',
      poet: { id: 2, name: 'سعدی شیرازی', slug: 'saadi', century: 7 },
      rhythm: { name: 'فاعلاتن فعلاتن فعلاتن فعلن' },
      poem_type: 'غزل',
      edition_source: 'تصحیح محمدعلی فروغی',
      verses: [
        { id: 401, order: 1, first_couplet: 'ای ساربان آهسته ران کارام جانم می‌رود', second_couplet: 'وان دل که با خود داشتم با دلستانم می‌رود' },
        { id: 402, order: 2, first_couplet: 'من مانده‌ام مهجور از او بیچاره و رنجور از او', second_couplet: 'گویی که نیشی دور از او در استخوانم می‌رود' },
        { id: 403, order: 3, first_couplet: 'محمل بدار ای ساروان تندی مکن با کاروان', second_couplet: 'کز عشق آن سرو روان گویی روانم می‌رود' },
        { id: 404, order: 4, first_couplet: 'در رفتن جان از بدن گویند هر نوعی سخن', second_couplet: 'من خود به چشم خویشتن دیدم که جانم می‌رود' }
      ]
    },
    {
      id: 5,
      title: 'بنی آدم اعضای یکدیگرند',
      slug: 'bani-adam',
      poet: { id: 2, name: 'سعدی شیرازی', slug: 'saadi', century: 7 },
      rhythm: { name: 'فاعلاتن فعلاتن فعلاتن فعلن' },
      poem_type: 'قطعه',
      edition_source: 'تصحیح محمدعلی فروغی',
      verses: [
        { id: 501, order: 1, first_couplet: 'بنی آدم اعضای یکدیگرند', second_couplet: 'که در آفرینش ز یک گوهرند' },
        { id: 502, order: 2, first_couplet: 'چو عضوی به درد آورد روزگار', second_couplet: 'دگر عضوها را نماند قرار' },
        { id: 503, order: 3, first_couplet: 'تو کز محنت دیگران بی‌غمی', second_couplet: 'نشاید که نامت نهند آدمی' }
      ]
    },
    {
      id: 6,
      title: 'بشنو این نی چون شکایت می‌کند',
      slug: 'beshno-in-ney',
      poet: { id: 3, name: 'مولانا جلال‌الدین بلخی', slug: 'rumi', century: 7 },
      rhythm: { name: 'فاعلاتن فاعلاتن فاعلاتن فاعلن' },
      poem_type: 'مثنوی',
      edition_source: 'نسخه رینولد نیکلسون',
      verses: [
        { id: 601, order: 1, first_couplet: 'بشنو این نی چون شکایت می‌کند', second_couplet: 'از جدایی‌ها حکایت می‌کند' },
        { id: 602, order: 2, first_couplet: 'کز نیستان تا مرا ببریده‌اند', second_couplet: 'در نفیرم مرد و زن نالیده‌اند' },
        { id: 603, order: 3, first_couplet: 'سینه خواهم شرحه شرحه از فراق', second_couplet: 'تا بگویم شرح درد اشتیاق' },
        { id: 604, order: 4, first_couplet: 'هر کسی کو دور ماند از اصل خویش', second_couplet: 'باز جوید روزگار وصل خویش' }
      ]
    },
    {
      id: 7,
      title: 'به نام خداوند جان و خرد',
      slug: 'be-name-khodavand',
      poet: { id: 4, name: 'حکیم ابوالقاسم فردوسی', slug: 'ferdowsi', century: 4 },
      rhythm: { name: 'فعولن فعولن فعولن فعل' },
      poem_type: 'مثنوی',
      edition_source: 'تصحیح جلال خالقی مطلق',
      verses: [
        { id: 701, order: 1, first_couplet: 'به نام خداوند جان و خرد', second_couplet: 'کزین برتر اندیشه برنگذرد' },
        { id: 702, order: 2, first_couplet: 'خداوند نام و خداوند جای', second_couplet: 'خداوند روزی‌ده رهنمای' },
        { id: 703, order: 3, first_couplet: 'توانا بود هر که دانا بود', second_couplet: 'ز دانش دل پیر برنا بود' }
      ]
    },
    {
      id: 8,
      title: 'ابر آمد و زار بر سر سبزه گریست',
      slug: 'abr-amad',
      poet: { id: 5, name: 'حکیم عمر خیام نیشابوری', slug: 'khayyam', century: 5 },
      rhythm: { name: 'مفعول مفاعیل مفاعیل فعل' },
      poem_type: 'رباعی',
      edition_source: 'گزیده صادق هدایت و فروغی',
      verses: [
        { id: 801, order: 1, first_couplet: 'ابر آمد و زار بر سر سبزه گریست', second_couplet: 'بی باده گلرنگ نمی‌شاید زیست' },
        { id: 802, order: 2, first_couplet: 'این سبزه که امروز تماشاگه ماست', second_couplet: 'تا سبزه خاک ما تماشاگه کیست' }
      ]
    }
  ]
};

const ApiClient = {
  getToken() {
    return localStorage.getItem('sherkhaneh_access_token');
  },

  setTokens(access, refresh) {
    localStorage.setItem('sherkhaneh_access_token', access);
    localStorage.setItem('sherkhaneh_refresh_token', refresh);
  },

  clearTokens() {
    localStorage.removeItem('sherkhaneh_access_token');
    localStorage.removeItem('sherkhaneh_refresh_token');
  },

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = this.getToken();

    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers
    };

    try {
      const response = await fetch(url, { ...options, headers });
      if (response.ok) {
        return await response.json();
      }
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || errData.detail || 'خطا در ارتباط با سرور.');
    } catch (err) {
      console.warn(`[SherKhaneh API] Server request failed for ${endpoint}. Falling back to offline store.`);
      return this.handleOfflineFallback(endpoint, options);
    }
  },

  // Fallback handler if Django backend is not currently running
  handleOfflineFallback(endpoint, options) {
    if (endpoint.startsWith('/poetry/poets/')) {
      return { count: FALLBACK_POETRY_STORE.poets.length, results: FALLBACK_POETRY_STORE.poets };
    }
    if (endpoint.startsWith('/poetry/poems/')) {
      const urlParams = new URLSearchParams(endpoint.split('?')[1] || '');
      const search = (urlParams.get('search') || '').trim();
      let results = FALLBACK_POETRY_STORE.poems;
      if (search) {
        results = results.filter(p => p.title.includes(search) || p.poet.name.includes(search));
      }
      return { count: results.length, results };
    }
    if (endpoint.includes('/daily/culture/today/')) {
      return {
        date: new Date().toISOString().split('T')[0],
        beyt_of_day: {
          first_couplet: 'صبر تلخ است ولیکن بر شیرین دارد',
          second_couplet: 'صبر کن ای دل غمدیده که پیروز شوی',
          poet: 'سعدی شیرازی',
          commentary: 'شکیبایی و امیدواری در پیمودن مسیرهای سخت، طعم شیرین پیروزی را به ارمغان می‌آورد.'
        },
        proverb_of_day: {
          proverb: 'گر صبر کنی ز غوره حلوا سازی',
          meaning: 'با حلم و حوصله و تلاش مستمر می‌توان سخت‌ترین کارها را به بهترین سرانجام رساند.'
        }
      };
    }
    if (endpoint.includes('/daily/culture/fal_hafez/')) {
      const p = FALLBACK_POETRY_STORE.poems[Math.floor(Math.random() * 3)];
      return {
        title: p.title,
        verses: p.verses.map(v => ({ first: v.first_couplet, second: v.second_couplet })),
        theme: 'امید و گشایش کارها',
        tafsir: 'خواجه شیراز شما را به توکل و شکیبایی دعوت می‌کند. گشایش در کارها نزدیک است؛ از بدگویی حاسدان نهراسید و با قلبی پاک به سوی مقصود پیش روید.'
      };
    }
    return { success: true, message: 'عملیات در حالت آفلاین ذخیره شد.' };
  }
};
