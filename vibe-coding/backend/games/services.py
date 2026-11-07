import random
from poetry.models import Poet, Poem, Verse
from .models import GameSession

CLASSICAL_WORDS_BANK = [
    {
        'word': 'میغ',
        'meaning': 'ابر باران‌زا',
        'distractors': ['باد تند', 'آفتاب تابان', 'رعد و برق'],
        'example_verse': 'ابر آمد و زار بر سر سبزه گریست / بی باده گلرنگ نمی‌شاید زیست'
    },
    {
        'word': 'خوالیگر',
        'meaning': 'طباخ و آشپز دربار',
        'distractors': ['سوارکار جنگی', 'خزانه‌دار', 'طبیب مخصوص'],
        'example_verse': 'چو خوالیگر آمد به نزدیک شاه / بیاراست خوان و بیامد سپاه'
    },
    {
        'word': 'تهمتن',
        'meaning': 'تنومند و پهلوان (لقب رستم)',
        'distractors': ['دانشمند زمانه', 'پادشاه عادل', 'فرمانده سواره‌نظام'],
        'example_verse': 'تهمتن برآویخت با شیر ژیان / کز او خیره ماندند گردن‌کشان'
    },
    {
        'word': 'سمن‌بر',
        'meaning': 'سپیدتن و زیبا همچون گل یاسمن',
        'distractors': ['جنگجوی چالاک', 'پیر دانا', 'سرکش و نامهربان'],
        'example_verse': 'بتی دیدم سمن‌بر ماه دیدار / دل و دین برده از من آشکار'
    },
    {
        'word': 'دستان',
        'meaning': 'نغمه و سرود یا افسون و نیرنگ (لقب زال)',
        'distractors': ['کتاب شعر', 'تیر و کمان', 'جام باده'],
        'example_verse': 'سرود و غزل‌های دستان‌سرای / دل خسته را کرد شادی‌فزای'
    },
    {
        'word': 'آبگینه',
        'meaning': 'شیشه و بلور شفاف',
        'distractors': ['سنگ خارا', 'شمشیر فولادی', 'طلا و زیور'],
        'example_verse': 'دل مرد دانا چو آبگینه است / در او نقش هر نیک و بد پیدا است'
    },
    {
        'word': 'خضر',
        'meaning': 'پیامبری که به آب حیات رسید و جاودانه شد',
        'distractors': ['شاعر دوران کهن', 'سپهدار توران', 'پادشاه روم'],
        'example_verse': 'گرت خضر باشد به ره رهنمای / به سرچشمه زندگی وارهان'
    }
]


def generate_guess_poet():
    """Generates a multiple choice question: guess poet from verse"""
    verses = list(Verse.objects.select_related('poem', 'poem__poet').all())
    if not verses:
        return None

    chosen = random.choice(verses)
    correct_poet = chosen.poem.poet

    all_poets = list(Poet.objects.exclude(id=correct_poet.id))
    distractors = random.sample(all_poets, min(3, len(all_poets)))

    options = [correct_poet.name] + [p.name for p in distractors]
    random.shuffle(options)

    return {
        'game_type': 'guess_poet',
        'verse': f"{chosen.first_couplet} / {chosen.second_couplet}",
        'poem_title': chosen.poem.title,
        'options': options,
        'correct_answer': correct_poet.name,
        'hint': f"این شاعر در سده «{correct_poet.century}» می‌زیسته است."
    }


def generate_next_couplet():
    """Generates a challenge where user must pick the second couplet"""
    verses = list(Verse.objects.select_related('poem', 'poem__poet').all())
    if len(verses) < 4:
        return None

    chosen = random.choice(verses)
    distractors = [v.second_couplet for v in random.sample([v for v in verses if v.id != chosen.id], 3)]

    options = [chosen.second_couplet] + distractors
    random.shuffle(options)

    return {
        'game_type': 'next_couplet',
        'first_couplet': chosen.first_couplet,
        'poet_name': chosen.poem.poet.name,
        'poem_title': chosen.poem.title,
        'options': options,
        'correct_answer': chosen.second_couplet
    }


def generate_word_quiz():
    """Generates archaic Persian word meaning quiz"""
    item = random.choice(CLASSICAL_WORDS_BANK)
    options = [item['meaning']] + item['distractors']
    random.shuffle(options)

    return {
        'game_type': 'word_quiz',
        'word': item['word'],
        'example_verse': item['example_verse'],
        'options': options,
        'correct_answer': item['meaning']
    }


def generate_bait_chin_game():
    """Generates a scrambled poem for bait-chin"""
    poems = list(Poem.objects.prefetch_related('verses').all())
    if not poems:
        return None

    chosen_poem = random.choice(poems)
    verses = list(chosen_poem.verses.all().order_by('order'))
    if len(verses) < 2:
        return None

    shuffled = [{
        'id': v.id,
        'text': f"{v.first_couplet} / {v.second_couplet}",
        'order': v.order
    } for v in verses]
    random.shuffle(shuffled)

    return {
        'game_type': 'bait_chin',
        'poem_id': chosen_poem.id,
        'poem_title': chosen_poem.title,
        'poet_name': chosen_poem.poet.name,
        'shuffled_verses': shuffled,
        'correct_sequence': [v.id for v in verses]
    }
