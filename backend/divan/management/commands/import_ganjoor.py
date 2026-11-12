import json
import urllib.request
from django.core.management.base import BaseCommand
from django.db import transaction
from divan.models import Poet, Work, Rhythm, Poem, Verse


class Command(BaseCommand):
    help = 'Import authentic poems from Ganjoor API into PostgreSQL.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--poet',
            type=str,
            default='سعدی',
            help='Poet name to search in Ganjoor (default: سعدی)'
        )
        parser.add_argument(
            '--offset',
            type=int,
            default=0,
            help='Number of poems to skip from the beginning (default: 0)'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of poems to fetch (default: 5)'
        )

    def fetch_json(self, url):
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'SherKhane/1.0'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))

    def fetch_wiki_summary(self, title):
        try:
            import urllib.parse
            encoded = urllib.parse.quote(title.replace(' ', '_'))
            url = f"https://fa.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            data = self.fetch_json(url)
            return data.get('extract')
        except Exception:
            return None

    def get_work_description(self, work_title, poet_name):
        nickname = poet_name.split()[0]
        queries = [
            f"{work_title} {poet_name}",
            f"{work_title} {nickname}",
        ]
        if 'دیوان' in work_title:
            queries.extend([f"دیوان {nickname}", f"کلیات {nickname}"])
        queries.append(work_title)

        for q in queries:
            desc = self.fetch_wiki_summary(q)
            if desc:
                return desc
        return f"مجموعه {work_title} از آثار و شاهکارهای ماندگار {poet_name} در گنجینه شعرخانه."

    def handle(self, *args, **options):
        poet_query = options['poet']
        fetch_limit = options['count']
        offset = options['offset']

        self.stdout.write(self.style.NOTICE(f'[INFO] Searching Ganjoor for poet: {poet_query}...'))

        # ۱. واکشی لیست تمام شاعران گنجور
        poets_data = self.fetch_json('https://api.ganjoor.net/api/ganjoor/poets')
        matched_poet = next((p for p in poets_data if poet_query in p['name']), None)

        if not matched_poet:
            self.stdout.write(self.style.ERROR(f'[ERROR] Poet "{poet_query}" was not found in Ganjoor.'))
            return

        poet_id = matched_poet['id']
        poet_name = matched_poet['name']
        root_cat_id = matched_poet['rootCatId']
        self.stdout.write(self.style.SUCCESS(f'[OK] Found poet: {poet_name} (Root Cat ID: {root_cat_id})'))

        # دریافت بیوگرافی کامل شاعر از صفحه اختصاصی
        poet_detail = self.fetch_json(f'https://api.ganjoor.net/api/ganjoor/poet/{poet_id}')
        full_bio = poet_detail.get('poet', {}).get('description') or f"شاعر پارسی‌گوی ثبت شده در گنجور. متولد {matched_poet.get('birthPlace', 'نامشخص')}."

        # ۲. واکشی دسته‌بندی‌های آثار شاعر جهت یافتن بخش غزلیات
        root_cat_data = self.fetch_json(f'https://api.ganjoor.net/api/ganjoor/cat/{root_cat_id}')
        children = root_cat_data.get('cat', {}).get('children', [])

        # جستجوی دیوان اشعار
        divan_cat = next((c for c in children if 'دیوان' in c['title']), None)
        target_cat_id = root_cat_id
        work_title = 'دیوان اشعار'
        work_desc = None

        if divan_cat:
            work_title = divan_cat['title']
            divan_data = self.fetch_json(f"https://api.ganjoor.net/api/ganjoor/cat/{divan_cat['id']}")
            work_desc = divan_data.get('cat', {}).get('description')
            sub_children = divan_data.get('cat', {}).get('children', [])
            ghazal_cat = next((c for c in sub_children if 'غزل' in c['title']), None)
            if ghazal_cat:
                target_cat_id = ghazal_cat['id']
            else:
                target_cat_id = divan_cat['id']

        if not work_desc:
            work_desc = self.get_work_description(work_title, poet_name)

        # ۳. دریافت لیست اشعار آن بخش
        target_data = self.fetch_json(f'https://api.ganjoor.net/api/ganjoor/cat/{target_cat_id}')
        raw_poems = target_data.get('cat', {}).get('poems', [])[offset : offset + fetch_limit]

        if not raw_poems:
            self.stdout.write(self.style.WARNING('[WARN] No poems found in this section.'))
            return

        self.stdout.write(self.style.NOTICE(f'[INFO] Selected {len(raw_poems)} poems to fetch.'))

        # ۴. ذخیره در دیتابیس درون یک تراکنش اتمیک
        with transaction.atomic():
            # تقریب قرن از روی سال وفات هجری قمری گنجور
            death_year = matched_poet.get('deathYearInLHijri')
            century = (death_year // 100) + 1 if death_year else None

            poet_obj, _ = Poet.objects.update_or_create(
                name=poet_name,
                defaults={
                    'century': century,
                    'bio': full_bio
                }
            )

            # ثبت یا به‌روزرسانی اثر (کتاب)
            work_obj, _ = Work.objects.update_or_create(
                poet=poet_obj,
                title=work_title,
                defaults={
                    'description': work_desc
                }
            )

            total_imported_verses = 0

            for p_summary in raw_poems:
                poem_id = p_summary['id']
                poem_detail = self.fetch_json(f'https://api.ganjoor.net/api/ganjoor/poem/{poem_id}')

                # استخراج وزن و بحر عروضی
                rhythm_obj = None
                sections = poem_detail.get('sections', [])
                if sections and sections[0].get('ganjoorMetre'):
                    metre_str = sections[0]['ganjoorMetre'].get('rhythm', '')
                    if metre_str:
                        rhythm_obj, _ = Rhythm.objects.get_or_create(name=metre_str[:100])

                # ثبت یا یافتن شعر
                poem_title = poem_detail.get('title', f"شعر شماره {poem_id}")
                poem_obj, created = Poem.objects.get_or_create(
                    poet=poet_obj,
                    title=f"{poet_name} - {poem_title}",
                    defaults={
                        'work': work_obj,
                        'poem_type': Poem.PoemType.GHAZAL,
                        'rhythm': rhythm_obj,
                    }
                )

                if not created:
                    poem_obj.verses.all().delete()
                    poem_obj.work = work_obj
                    poem_obj.rhythm = rhythm_obj
                    poem_obj.save()

                # استخراج ابیات از روی جفت مصرع‌ها
                verses_data = poem_detail.get('verses', [])
                couplets_dict = {}
                for v in verses_data:
                    c_idx = v['coupletIndex']
                    if c_idx not in couplets_dict:
                        couplets_dict[c_idx] = {'first': '', 'second': ''}
                    if v['versePosition'] == 0:
                        couplets_dict[c_idx]['first'] = v['text']
                    else:
                        couplets_dict[c_idx]['second'] = v['text']

                verse_instances = [
                    Verse(
                        poem=poem_obj,
                        order=idx + 1,
                        first_couplet=c_data['first'],
                        second_couplet=c_data['second'],
                    )
                    for idx, c_data in couplets_dict.items()
                    if c_data['first'] and c_data['second']
                ]

                Verse.objects.bulk_create(verse_instances)
                total_imported_verses += len(verse_instances)

                self.stdout.write(f"  - {poem_obj.title} ({len(verse_instances)} couplets) -> Saved")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n[SUCCESS] Imported {len(raw_poems)} poems and {total_imported_verses} couplets into the database."
            )
        )