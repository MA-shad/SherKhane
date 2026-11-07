from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from accounts.models import User, UserProfile
from poetry.models import Poet, Poem, Verse
from memorization.models import MemorizationItem
from memorization.services import calculate_sm2_schedule, generate_cloze_challenge


class MemorizationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hafez_khan', password='Password123!')
        UserProfile.objects.create(user=self.user, display_name='حافظ‌خوان')
        self.poet = Poet.objects.create(name='حافظ', slug='hafez')
        self.poem = Poem.objects.create(poet=self.poet, title='شعر تست', slug='test-poem')
        self.verse = Verse.objects.create(
            poem=self.poem,
            order=1,
            first_couplet='صلاح کار کجا و من خراب کجا',
            second_couplet='ببین تفاوت ره از کجاست تا به کجا'
        )

    def test_sm2_successful_progression(self):
        item = MemorizationItem.objects.create(user=self.user, poem=self.poem)
        self.assertEqual(item.repetition_count, 0)
        self.assertEqual(item.mastery_level, MemorizationItem.MasteryLevel.NOVICE)

        # Grade 5 (Perfect recall)
        calculate_sm2_schedule(item, quality_grade=5)
        item.refresh_from_db()

        self.assertEqual(item.repetition_count, 1)
        self.assertEqual(item.interval_days, 1)
        self.assertEqual(item.mastery_level, MemorizationItem.MasteryLevel.LEARNING)
        self.assertGreaterEqual(self.user.profile.xp_points, 120)

    def test_sm2_failed_recall_resets(self):
        item = MemorizationItem.objects.create(
            user=self.user,
            poem=self.poem,
            repetition_count=3,
            interval_days=7,
            mastery_level=MemorizationItem.MasteryLevel.REVIEWING
        )

        # Grade 1 (Blackout failure)
        calculate_sm2_schedule(item, quality_grade=1)
        item.refresh_from_db()

        self.assertEqual(item.repetition_count, 0)
        self.assertEqual(item.interval_days, 1)
        self.assertEqual(item.mastery_level, MemorizationItem.MasteryLevel.LEARNING)

    def test_cloze_challenge_generation(self):
        exercises = generate_cloze_challenge(self.poem)
        self.assertEqual(len(exercises), 1)
        self.assertIn('____', exercises[0]['masked_couplet'])
        self.assertTrue(len(exercises[0]['missing_word']) >= 2)
