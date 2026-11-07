import random
from django.utils import timezone
from core.normalizer import (
    normalize_persian_text,
    extract_starting_letter,
    extract_rhyme_letter
)
from poetry.models import Verse
from .models import MushaerehRoom, MushaerehTurn


def letters_match(char1: str, char2: str) -> bool:
    """Check Persian letter equivalence (e.g., آ and ا, etc.)"""
    c1 = normalize_persian_text(char1)
    c2 = normalize_persian_text(char2)
    return c1 == c2


def submit_user_verse(room: MushaerehRoom, verse_text: str, user=None):
    """
    Validates and applies user submission in server-authoritative Mushaereh.
    """
    if room.status != MushaerehRoom.Status.ACTIVE:
        return {'success': False, 'error': 'این مسابقه به پایان رسیده است.'}

    # Clean text
    clean_text = verse_text.strip()
    if len(clean_text) < 10:
        return {'success': False, 'error': 'متن بیت بسیار کوتاه است. لطفاً حداقل یک مصراع کامل بنویسید.'}

    # 1. Starting letter check
    start_letter = extract_starting_letter(clean_text)
    if not letters_match(start_letter, room.current_letter):
        return {
            'success': False,
            'error': f"بیت شما با حرف «{start_letter}» آغاز شده است، در حالی که نوبت با حرف «{room.current_letter}» بود."
        }

    # 2. Duplicate verse check in current room
    norm_submission = normalize_persian_text(clean_text)
    existing_turns = room.turns.filter(is_valid=True)
    for t in existing_turns:
        if normalize_persian_text(t.verse_text) == norm_submission:
            return {'success': False, 'error': 'این بیت قبلاً در این مسابقه خوانده شده است. تکرار بیت در مشاعره خطا محسوب می‌شود.'}

    # 3. Ending letter extraction
    end_letter = extract_rhyme_letter(clean_text)
    if not end_letter:
        return {'success': False, 'error': 'حرف پایانی بیت قابل تشخیص نیست.'}

    # Record valid turn
    next_turn_no = room.turns.count() + 1
    player_name = user.profile.display_name if (user and hasattr(user, 'profile') and user.profile.display_name) else (user.username if user else 'کاربر')

    turn = MushaerehTurn.objects.create(
        room=room,
        turn_number=next_turn_no,
        player_name=player_name,
        verse_text=clean_text,
        poet_name='شعر کاربر',
        starting_letter=start_letter,
        ending_letter=end_letter,
        is_valid=True
    )

    room.score_user += 10
    room.rounds_completed += 1
    room.current_letter = end_letter
    room.current_turn = 'bot' if room.mode == MushaerehRoom.Mode.BOT else 'opponent'
    room.turn_start_time = timezone.now()
    room.save()

    if user and hasattr(user, 'profile'):
        user.profile.add_xp(15)

    bot_turn_data = None
    if room.mode == MushaerehRoom.Mode.BOT:
        bot_turn_data = play_bot_turn(room)

    return {
        'success': True,
        'user_turn': {
            'turn_number': turn.turn_number,
            'player_name': turn.player_name,
            'verse_text': turn.verse_text,
            'starting_letter': turn.starting_letter,
            'ending_letter': turn.ending_letter
        },
        'bot_turn': bot_turn_data,
        'room': {
            'current_letter': room.current_letter,
            'score_user': room.score_user,
            'score_opponent': room.score_opponent,
            'rounds_completed': room.rounds_completed,
            'status': room.status
        }
    }


def play_bot_turn(room: MushaerehRoom):
    """
    AI Poet (سخن‌سنج) responds with an authentic classical verse starting with the current letter.
    """
    target_letter = room.current_letter
    used_verses = set(room.turns.filter(is_valid=True).values_list('verse_text', flat=True))

    # Search in database for verses whose first couplet starts with target_letter
    candidates = []
    verses = Verse.objects.select_related('poem', 'poem__poet').all()
    for v in verses:
        v_start = extract_starting_letter(v.first_couplet)
        if letters_match(v_start, target_letter):
            full_verse = f"{v.first_couplet} / {v.second_couplet}"
            if full_verse not in used_verses:
                candidates.append((v, full_verse))

    if not candidates:
        # Bot couldn't find a verse -> User wins!
        room.status = MushaerehRoom.Status.FINISHED
        room.save()
        return {
            'player_name': 'سخن‌سنج (ربات)',
            'verse_text': 'هوش سخن‌سنج در برابر طبع شما تسلیم شد! شما پیروز این مسابقه شدید.',
            'poet_name': 'پایان مسابقه',
            'starting_letter': target_letter,
            'ending_letter': '',
            'winner': 'user'
        }

    # Pick a random candidate
    chosen_verse, full_verse_text = random.choice(candidates)
    end_letter = extract_rhyme_letter(chosen_verse.second_couplet)

    bot_turn_no = room.turns.count() + 1
    bot_turn = MushaerehTurn.objects.create(
        room=room,
        turn_number=bot_turn_no,
        player_name='سخن‌سنج (ربات)',
        verse_text=full_verse_text,
        poet_name=chosen_verse.poem.poet.name,
        starting_letter=target_letter,
        ending_letter=end_letter,
        is_valid=True
    )

    room.score_opponent += 10
    room.rounds_completed += 1
    room.current_letter = end_letter
    room.current_turn = 'user'
    room.turn_start_time = timezone.now()
    room.save()

    return {
        'turn_number': bot_turn.turn_number,
        'player_name': bot_turn.player_name,
        'verse_text': bot_turn.verse_text,
        'poet_name': bot_turn.poet_name,
        'starting_letter': bot_turn.starting_letter,
        'ending_letter': bot_turn.ending_letter
    }
