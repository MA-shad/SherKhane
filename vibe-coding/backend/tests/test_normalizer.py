from django.test import TestCase
from core.normalizer import (
    normalize_persian_text,
    extract_rhyme_letter,
    extract_starting_letter,
    calculate_verse_similarity
)


class PersianNormalizerTests(TestCase):
    def test_arabic_substitution(self):
        raw = "سعدي در كتاب گلستان فرمود"
        expected = "سعدی در کتاب گلستان فرمود"
        self.assertEqual(normalize_persian_text(raw), expected)

    def test_diacritics_and_tatweel_removal(self):
        raw = "بَنی‌آدَم اَعضایِ یِکدیگَرَند سَـــــعدی"
        expected = "بنی ادم اعضای یکدیگرند سعدی"
        self.assertEqual(normalize_persian_text(raw), expected)

    def test_extract_starting_letter(self):
        verse = "  «الا یا ایها الساقی ادر کأسا و ناولها»  "
        self.assertEqual(extract_starting_letter(verse), 'ا')

    def test_extract_rhyme_letter(self):
        verse = "که عشق آسان نمود اول ولی افتاد مشکل‌ها!..."
        self.assertEqual(extract_rhyme_letter(verse), 'ا')

    def test_verse_similarity(self):
        v1 = "یوسف گمگشته بازآید به کنعان غم مخور"
        v2 = "یوسف گمگشته باز اید به کنعان غم مخور"
        similarity = calculate_verse_similarity(v1, v2)
        self.assertGreaterEqual(similarity, 0.65)
