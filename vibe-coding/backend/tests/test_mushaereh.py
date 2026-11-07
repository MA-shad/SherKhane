from django.test import TestCase
from accounts.models import User, UserProfile
from poetry.models import Poet, Poem, Verse
from mushaereh.models import MushaerehRoom
from mushaereh.services import submit_user_verse


class MushaerehServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mushaereh_baz', password='Password123!')
        UserProfile.objects.create(user=self.user, display_name='شاعر جوان')
        self.poet = Poet.objects.create(name='سعدی', slug='saadi')
        self.poem = Poem.objects.create(poet=self.poet, title='شعر سعدی', slug='poem-saadi')
        Verse.objects.create(
            poem=self.poem,
            order=1,
            first_couplet='درخت دوستی بنشان که کام دل به بار آرد',
            second_couplet='نهال دشمنی برکن که رنج بی‌شمار آرد'
        )

    def test_valid_verse_submission(self):
        room = MushaerehRoom.objects.create(
            creator=self.user,
            current_letter='ب',
            mode=MushaerehRoom.Mode.BOT
        )
        verse = "بنی آدم اعضای یکدیگرند / که در آفرینش ز یک گوهرند"
        result = submit_user_verse(room, verse, user=self.user)

        self.assertTrue(result['success'])
        room.refresh_from_db()
        self.assertEqual(room.score_user, 10)
        self.assertEqual(room.rounds_completed, 2)  # User + Bot

    def test_wrong_letter_rejection(self):
        room = MushaerehRoom.objects.create(
            creator=self.user,
            current_letter='م',
            mode=MushaerehRoom.Mode.BOT
        )
        verse = "سعدیا مرد نکونام نمیرد هرگز"
        result = submit_user_verse(room, verse, user=self.user)

        self.assertFalse(result['success'])
        self.assertIn('با حرف «س» آغاز شده است', result['error'])

    def test_duplicate_verse_prevention(self):
        room = MushaerehRoom.objects.create(
            creator=self.user,
            current_letter='ب',
            mode=MushaerehRoom.Mode.MULTIPLAYER
        )
        verse = "بنی آدم اعضای یکدیگرند / که در آفرینش ز یک گوهرند"
        res1 = submit_user_verse(room, verse, user=self.user)
        self.assertTrue(res1['success'])

        # Try submitting identical verse again in same match
        room.current_letter = 'ب'
        room.save()
        res2 = submit_user_verse(room, verse, user=self.user)
        self.assertFalse(res2['success'])
        self.assertIn('قبلاً در این مسابقه خوانده شده', res2['error'])
