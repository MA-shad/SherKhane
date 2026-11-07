import random
from django.utils import timezone
from poetry.models import Poem, Poet
from .models import DailyHighlight

DAILY_HIGHLIGHTS_COLLECTION = [
    {
        'beyt_first': 'صبر تلخ است ولیکن بر شیرین دارد',
        'beyt_second': 'صبر کن ای دل غمدیده که پیروز شوی',
        'poet_name': 'سعدی شیرازی',
        'poetic_commentary': 'شکیبایی و استقامت در راه هدف، همواره تلخی مقطعی را به حلاوت جاودان پیروزی پیوند می‌زند.',
        'proverb': 'گر صبر کنی ز غوره حلوا سازی',
        'proverb_meaning': 'انسان با شکیبایی، بردباری و استمرار می‌تواند سخت‌ترین و ناممکن‌ترین امور را به بهترین فرجام برساند.',
        'proverb_origin': 'ریشه در امثال‌وحکم دهخدا و شعری منسوب به کهن‌سرایان ادب پارسی دارد.'
    },
    {
        'beyt_first': 'در ناامیدی بسی امید است',
        'beyt_second': 'پایان شب سیه سپید است',
        'poet_name': 'نظامی گنجوی',
        'poetic_commentary': 'حکیم نظامی در منظومه خسرو و شیرین، امید را چراغ فروزان دل سالک در اوج تاریکی‌ها می‌داند.',
        'proverb': 'پایان شب سیه سپید است',
        'proverb_meaning': 'هیچ سختی و اندوهی پایدار نخواهد ماند و در پی هر دشواری، گشایش و روشنی خواهد بود.',
        'proverb_origin': 'برگرفته از داستان‌های عاشقانه خمسه نظامی گنجوی.'
    },
    {
        'beyt_first': 'درخت دوستی بنشان که کام دل به بار آرد',
        'beyt_second': 'نهال دشمنی برکن که رنج بی‌شمار آرد',
        'poet_name': 'حافظ شیرازی',
        'poetic_commentary': 'حافظ مهرورزی و یکدلی را جوهره حیات انسان و پیشگیری‌کننده از کینه‌های ویرانگر می‌خواند.',
        'proverb': 'دل به دل راه دارد',
        'proverb_meaning': 'محبت و صداقت قلبی به طور ناخودآگاه در دل طرف مقابل نیز احساسی مشابه ایجاد می‌نماید.',
        'proverb_origin': 'از ضرب‌المثل‌های کهن مردمی بازتاب‌یافته در شعر حافظ و صائب تبریزی.'
    }
]

HAFEZ_TAFSIR_TEMPLATES = [
    {
        'theme': 'امید و گشایش امور',
        'tafsir': 'خواجه شیراز شما را به شکیبایی، توکل و امیدواری فرا می‌خواند. اگر در کار یا هدفی نیت کرده‌اید، موانع کنونی گذرا هستند. از سرزنش بدخواهان نهراسید و با توکل بر پروردگار، گام در راه بگذارید که پایان این شام تاریک، سپیده روشن است.'
    },
    {
        'theme': 'محبت، صداقت و پرهیز از تظاهر',
        'tafsir': 'نیت شما نشان از دلی پاک و باصفا دارد، اما مراقب ریاکاری و دورنگی اطرافیان باشید. صداقت و صمیمیت را پیشه خود سازید و اسرار دل را با هر نامحرمی در میان مگذارید. با یاران راستین هم‌نشین شوید تا آرامش خاطر نصیبتان گردد.'
    },
    {
        'theme': 'تلاش، شجاعت و دوری از تردید',
        'tafsir': 'وقت آن رسیده است که تردید و دودلی را کنار بگذارید. فرصت‌های ارزشمندی پیش روی شماست که غفلت از آن‌ها حسرت به بار خواهد آورد. با مشورت و همت بلند اقدام کنید و به وعده‌های فریبنده دنیا دل مبندید.'
    }
]


def get_or_create_today_highlight():
    today = timezone.now().date()
    highlight = DailyHighlight.objects.filter(date=today).first()
    if not highlight:
        # Pick one from collection or cycle by day
        idx = today.toordinal() % len(DAILY_HIGHLIGHTS_COLLECTION)
        data = DAILY_HIGHLIGHTS_COLLECTION[idx]
        highlight = DailyHighlight.objects.create(
            date=today,
            beyt_first=data['beyt_first'],
            beyt_second=data['beyt_second'],
            poet_name=data['poet_name'],
            poetic_commentary=data['poetic_commentary'],
            proverb=data['proverb'],
            proverb_meaning=data['proverb_meaning'],
            proverb_origin=data['proverb_origin']
        )
    return highlight


def draw_fal_hafez():
    """
    Draw an authentic Faal from Hafez ghazals with respectful literary commentary.
    """
    hafez_poet = Poet.objects.filter(slug='hafez').first()
    hafez_poems = Poem.objects.filter(poet=hafez_poet).prefetch_related('verses')
    if not hafez_poems.exists():
        hafez_poems = Poem.objects.prefetch_related('verses')

    if not hafez_poems.exists():
        return None

    poem = random.choice(list(hafez_poems))
    verses_list = [
        {'order': v.order, 'first': v.first_couplet, 'second': v.second_couplet}
        for v in poem.verses.all().order_by('order')
    ]

    # Select respectful literary interpretation
    tafsir_choice = random.choice(HAFEZ_TAFSIR_TEMPLATES)

    first_verse_text = ""
    if verses_list:
        first_verse_text = f"{verses_list[0]['first']} / {verses_list[0]['second']}"

    return {
        'poem_id': poem.id,
        'title': poem.title,
        'mطلع': first_verse_text,
        'verses': verses_list,
        'theme': tafsir_choice['theme'],
        'tafsir': tafsir_choice['tafsir'],
        'edition': poem.edition_source or 'دیوان خواجه شمس‌الدین محمد حافظ شیرازی'
    }
