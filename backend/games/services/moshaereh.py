import re
from typing import Optional, Tuple
from django.db.models import QuerySet
from divan.models import Verse
from games.models import MoshaerehSession


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