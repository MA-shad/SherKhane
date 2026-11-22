import re
from typing import Optional, Tuple
from django.db.models import QuerySet
from divan.models import Verse
from games.models import MoshaerehSession
import random


ARABIC_TO_PERSIAN_MAP = {
    'ي': 'ی',
    'ك': 'ک',
    'ة': 'ه',
    'ۀ': 'ه',
    'ؤ': 'و',
    'إ': 'ا',
    'أ': 'ا',
    'ء': '',
}

DIARITICS_PATTERN = re.compile(
    r'[\u064b-\u065f\u0670\u0640]'
    )

NON_ALPHABETIC_PATTERN = re.compile(
    r'[^آ-ی\s]'
)

def normalize_persian_text(text: str) -> str:
    if not text:
        return ""

    cleaned = text.strip()
    for ar_char, fa_char in ARABIC_TO_PERSIAN_MAP.items():
        cleaned = cleaned.replace(ar_char, fa_char)
        
    cleaned = DIARITICS_PATTERN.sub('', cleaned)
    cleaned = NON_ALPHABETIC_PATTERN.sub('', cleaned)
    cleaned = re.sub(r'\s+',' ', cleaned).strip()
    return cleaned

def extract_first_letter(couplet_text: str) -> Optional[str]:
    normalize = normalize_persian_text(couplet_text)
    if not normalize:
        return None
    return normalize[0]

def extract_last_letter(couplet_text: str) -> Optional[str]:
    normalized = normalize_persian_text(couplet_text)
    if not normalized:
        return None
    return normalized[-1]

def find_system_response_verse(target_letter: str, used_verse_ids: list[int]) -> Optional[Verse]:
    candidate_verses = Verse.objects.exclude(
        id__in=used_verse_ids
    ).filter(
        first_couplet__istartswith=target_letter
    ).select_related(
        'poem', 'poem__poet'
    ).order_by('?')[:25]
    matched_verses = [
        verse for verse in candidate_verses
        if extract_first_letter(verse.first_couplet) == target_letter
    ]   
    
    if matched_verses:
        return random.choice(matched_verses)
    return None

def play_mushaereh_turn(session: MoshaerehSession, user_verse_text: str) -> Tuple[bool, str, Optional[Verse]]:
    if not session.is_active:
        return False, "این بازی به پایان رسیده است.", None

    normalized_user_verse = normalize_persian_text(user_verse_text)
    if len(normalized_user_verse) < 5:
        return False, "متن وارد شده برای یک بیت بسیار کوتاه است.", None
    
    user_start_letter = extract_first_letter(normalized_user_verse)
    if user_start_letter != session.current_letter:
        return False, f"حرف اول بیت شما باید «{session.current_letter}» باشد، اما با «{user_start_letter}» آغاز شده است.", None

    user_end_letter = extract_last_letter(normalized_user_verse)
    if not user_end_letter:
        return False, "امکان استخراج حرف آخر از شعر ارسالی وجود ندارد.", None
    
    used_ids = list(session.used_verse.values_list('id', flat=True))
    bot_verse = find_system_response_verse(user_end_letter, used_ids)
    if not bot_verse:
        session.score += 20
        session.is_active = False
        session.save()
        return True, "آفرین! گنجینه شعرخانه در برابر این حرف بیتی نیافت و شما برنده این مسابقه شدید!", None

    session.used_verse.add(bot_verse)
    next_letter_for_user = extract_last_letter(bot_verse.second_couplet or bot_verse.first_couplet)

    session.score += 10
    session.round_count += 1
    session.current_letter = next_letter_for_user or 'م'
    session.save()

    return True, "بیت شما معتبر بود و پاسخ سامانه ثبت گردید.", bot_verse

