import random
from datetime import timedelta
from django.utils import timezone
from .models import MemorizationItem, MemorizationLog


def calculate_sm2_schedule(item: MemorizationItem, quality_grade: int):
    """
    Standard SuperMemo-2 (SM-2) algorithm adapted for Persian poetry memorization.
    quality_grade: 0 to 5
    """
    today = timezone.now().date()
    item.total_attempts += 1
    item.last_reviewed_at = timezone.now()

    # Update Easiness Factor (EF)
    new_ef = item.easiness_factor + (0.1 - (5 - quality_grade) * (0.08 + (5 - quality_grade) * 0.02))
    item.easiness_factor = max(1.3, round(new_ef, 2))

    if quality_grade >= 3:
        # Successful recall
        item.total_correct += 1
        if item.repetition_count == 0:
            item.interval_days = 1
        elif item.repetition_count == 1:
            item.interval_days = 3
        elif item.repetition_count == 2:
            item.interval_days = 7
        else:
            item.interval_days = int(round(item.interval_days * item.easiness_factor))

        item.repetition_count += 1

        # Update Mastery Level
        if item.repetition_count >= 6:
            item.mastery_level = MemorizationItem.MasteryLevel.MASTERED
        elif item.repetition_count >= 3:
            item.mastery_level = MemorizationItem.MasteryLevel.REVIEWING
        else:
            item.mastery_level = MemorizationItem.MasteryLevel.LEARNING

        # Reward XP
        if hasattr(item.user, 'profile'):
            item.user.profile.add_xp(25)
    else:
        # Failed recall - reset repetition count to reinforce memory
        item.repetition_count = 0
        item.interval_days = 1
        item.mastery_level = MemorizationItem.MasteryLevel.LEARNING

        if hasattr(item.user, 'profile'):
            item.user.profile.add_xp(5)

    item.next_review_date = today + timedelta(days=item.interval_days)
    item.save()

    # Create log entry
    MemorizationLog.objects.create(
        item=item,
        quality_grade=quality_grade,
        exercise_type='active_recall'
    )
    return item


def generate_cloze_challenge(poem):
    """
    Generates fill-in-the-blank (جای خالی) cloze test for each verse.
    Picks one significant word (> 3 characters) to mask.
    """
    exercises = []
    for verse in poem.verses.all().order_by('order'):
        couplet_target = 1 if (verse.order % 2 == 1) else 2
        couplet_text = verse.first_couplet if couplet_target == 1 else verse.second_couplet
        words = couplet_text.split()

        # Candidates are words longer than 3 chars
        candidates = [w for w in words if len(w) >= 3 and not w.startswith(('که', 'از', 'به', 'با', 'در'))]
        if not candidates:
            candidates = words

        target_word = random.choice(candidates)
        # Create masked text
        masked_couplet = couplet_text.replace(target_word, '____', 1)

        exercises.append({
            'verse_order': verse.order,
            'full_first': verse.first_couplet,
            'full_second': verse.second_couplet,
            'target_couplet': couplet_target,
            'masked_couplet': masked_couplet,
            'missing_word': target_word,
            'hint': f"حرف اول: «{target_word[0]}»"
        })

    return exercises


def generate_scramble_challenge(poem):
    """
    Generates scrambled verses (بیت‌چین) where verses are shuffled and user re-orders them.
    """
    verses = list(poem.verses.all().order_by('order'))
    items = [{
        'id': v.id,
        'order': v.order,
        'text': f"{v.first_couplet} / {v.second_couplet}"
    } for v in verses]

    shuffled = list(items)
    random.shuffle(shuffled)

    return {
        'poem_id': poem.id,
        'poem_title': poem.title,
        'poet_name': poem.poet.name,
        'shuffled_verses': shuffled,
        'correct_order_ids': [v.id for v in verses]
    }
