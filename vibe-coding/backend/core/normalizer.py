import re
import unicodedata

# Arabic & Persian character mapping
CHAR_MAP = {
    'ي': 'ی',
    'ى': 'ی',
    'ك': 'ک',
    'ة': 'ه',
    'ۀ': 'ه',
    'هٔ': 'ه',
    'آ': 'ا',
    'أ': 'ا',
    'إ': 'ا',
    'ؤ': 'و',
    'ئ': 'ی',
}

# Diacritics regex
DIACRITICS_REGEX = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]')
TATWEEL_REGEX = re.compile(r'\u0640')
PUNCTUATION_REGEX = re.compile(r'[\.,،؛:\!\?؟\-_\(\)\[\]\{\}«»\"\'\s]+')


def normalize_persian_text(text: str, keep_zwnj: bool = False) -> str:
    """
    Standardize Persian text:
    - Replaces Arabic letters with Persian equivalents (ی, ک, etc.)
    - Removes vowels, tanwin, and diacritics
    - Removes tatweel (کشیده)
    - Normalizes extra whitespaces
    """
    if not text:
        return ""

    # Normalize unicode
    text = unicodedata.normalize('NFKC', text)

    # Character substitutions
    for ar_char, fa_char in CHAR_MAP.items():
        text = text.replace(ar_char, fa_char)

    # Remove diacritics
    text = DIACRITICS_REGEX.sub('', text)

    # Remove tatweel
    text = TATWEEL_REGEX.sub('', text)

    if not keep_zwnj:
        # Replace ZWNJ with standard space for search indexing
        text = text.replace('\u200c', ' ')

    # Compress multiple whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_rhyme_letter(verse: str) -> str:
    """
    Extract the effective ending Persian letter of a verse for Mushaereh rules.
    Ignores punctuation, quotes, and whitespace.
    """
    if not verse:
        return ""

    cleaned = normalize_persian_text(verse, keep_zwnj=False)
    # Filter only Persian letters
    letters = [ch for ch in cleaned if ch.isalnum()]
    if not letters:
        return ""
    last_char = letters[-1]

    # Special rule: silent 'ه' (ه غیر ملفوظ) is often treated as 'ه' or 'ا'
    return last_char


def extract_starting_letter(verse: str) -> str:
    """
    Extract the first significant Persian letter of a verse for Mushaereh validation.
    """
    if not verse:
        return ""

    cleaned = normalize_persian_text(verse, keep_zwnj=False)
    letters = [ch for ch in cleaned if ch.isalnum()]
    if not letters:
        return ""
    return letters[0]


def calculate_verse_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity between 0.0 and 1.0 for fill-in-the-blank and recall exercises.
    """
    s1 = normalize_persian_text(str1)
    s2 = normalize_persian_text(str2)
    if not s1 or not s2:
        return 0.0
    if s1 == s2:
        return 1.0

    words1 = set(s1.split())
    words2 = set(s2.split())
    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union)
