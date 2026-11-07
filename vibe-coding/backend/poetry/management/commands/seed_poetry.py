import sys
from django.core.management.base import BaseCommand
from poetry.models import Poet, Rhythm, Work, Poem, Verse

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class Command(BaseCommand):
    help = 'Seeds the database with authentic, high-quality classical Persian poetry'

    def handle(self, *args, **options):
        self.stdout.write("Seeding classical Persian poetry...")

        # 1. Rhythms (اوزان عروضی)
        rhythms_data = [
            {
                'name': 'فاعلاتن فعلاتن فعلاتن فعلن',
                'bahr': 'بحر رمل مثمن مخبون محذوف',
                'pattern': '- - v - / v - - - / v - - - / v -'
            },
            {
                'name': 'مفاعیلن مفاعیلن فعولن',
                'bahr': 'بحر هزج مسدس محذوف',
                'pattern': 'v - - - / v - - - / v - -'
            },
            {
                'name': 'فاعلاتن فاعلاتن فاعلاتن فاعلن',
                'bahr': 'بحر رمل مثمن محذوف',
                'pattern': '- v - - / - v - - / - v - - / - v -'
            },
            {
                'name': 'فعولن فعولن فعولن فعل',
                'bahr': 'بحر متقارب مثمن محذوف (وزن حماسی شاهنامه)',
                'pattern': 'v - - / v - - / v - - / v -'
            },
            {
                'name': 'مفعول مفاعیل مفاعیل فعل',
                'bahr': 'بحر هزج مثمن اخرب مکفوف مجبوب (وزن رباعی)',
                'pattern': '- - v / v - - v / v - - v / v -'
            },
            {
                'name': 'مفتعلن فاعلات مفتعلن فع',
                'bahr': 'بحر منسرح مثمن مطوی مکشوف',
                'pattern': '- v v - / - v - v / - v v - / -'
            },
            {
                'name': 'مفاعیلن مفاعیلن مفاعیلن مفاعیلن',
                'bahr': 'بحر هزج مثمن سالم',
                'pattern': 'v - - - / v - - - / v - - - / v - - -'
            }
        ]
        rhythm_objs = {}
        for r in rhythms_data:
            obj, _ = Rhythm.objects.get_or_create(name=r['name'], defaults={'bahr': r['bahr'], 'pattern': r['pattern']})
            rhythm_objs[r['name']] = obj

        # 2. Poets (شاعران بزرگ)
        poets_data = [
            {
                'name': 'حافظ شیرازی',
                'slug': 'hafez',
                'bio': 'خواجه شمس‌الدین محمد بن بهاءالدّین حافظ شیرازی (زاده ح. ۷۲۷ ه‍.ق – درگذشته ۷۹۲ ه‍.ق) نامور به لسان‌الغیب و ترجمان‌الاسرار، غزل‌سرای بزرگ زبان فارسی و یکی از سخن‌وران جهان است.',
                'century': 8,
                'birth_place': 'شیراز',
                'avatar': 'hafez.jpg'
            },
            {
                'name': 'سعدی شیرازی',
                'slug': 'saadi',
                'bio': 'ابومحمّد مُشرف‌الدین مُصلِح بن عبدالله بن مشرّف شیرازی (زاده ۵۸۵ یا ۶۰۶ ه‍.ق – درگذشته ۶۹۰ یا ۶۹۴ ه‍.ق) متخلص به سعدی، نامور به استاد سخن و شیخ اجل، پادشاه سخن در نظم و نثر پارسی است.',
                'century': 7,
                'birth_place': 'شیراز',
                'avatar': 'saadi.jpg'
            },
            {
                'name': 'مولانا جلال‌الدین بلخی',
                'slug': 'rumi',
                'bio': 'جلال‌الدین محمد بلخی رومی (زاده ۶۰۴ ه‍.ق در بلخ – درگذشته ۶۷۲ ه‍.ق در قونیه) مشهور به مولوی یا رومی، از بزرگ‌ترین سرایندگان و عارفان شورانگیز زبان پارسی و صاحب دیوان کبیر شمس و مثنوی معنوی است.',
                'century': 7,
                'birth_place': 'بلخ',
                'avatar': 'rumi.jpg'
            },
            {
                'name': 'حکیم ابوالقاسم فردوسی',
                'slug': 'ferdowsi',
                'bio': 'ابوالقاسم فردوسی طوسی (زاده ۳۲۹ ه‍.ق – درگذشته ۴۱۱ یا ۴۱۶ ه‍.ق در توس)، حماسه‌سرای بزرگ تاریخ ایران و آفریننده شاهنامه، شاهکار بی‌بدیل هویت ملی و ادب فارسی است.',
                'century': 4,
                'birth_place': 'توس',
                'avatar': 'ferdowsi.jpg'
            },
            {
                'name': 'حکیم عمر خیام نیشابوری',
                'slug': 'khayyam',
                'bio': 'غیاث‌الدین ابوالفتح عمر بن ابراهیم خیام نیشابوری (زاده ۴۳۹ ه‍.ق – درگذشته ۵۱۷ ه‍.ق) فیلسوف، ریاضیدان، اخترشناس و سراینده برجسته رباعیات شگفت‌انگیز فارسی است.',
                'century': 5,
                'birth_place': 'نیشابور',
                'avatar': 'khayyam.jpg'
            },
            {
                'name': 'حکیم نظامی گنجوی',
                'slug': 'nezami',
                'bio': 'جمال‌الدین ابومحمّد الیاس بن یوسف بن زکی بن مؤیَّد ملقب به نظامی گنجوی (زاده ۵۳۵ ه‍.ق – درگذشته ۶۰۲ ه‍.ق در گنجه) پیشوای بی‌همتای داستان‌سرایی و منظومه‌های غنایی در زبان فارسی است.',
                'century': 6,
                'birth_place': 'گنجه',
                'avatar': 'nezami.jpg'
            }
        ]
        poet_objs = {}
        for p in poets_data:
            obj, _ = Poet.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'name': p['name'],
                    'bio': p['bio'],
                    'century': p['century'],
                    'birth_place': p['birth_place'],
                    'avatar': p['avatar']
                }
            )
            poet_objs[p['slug']] = obj

        # 3. Works (آثار معتبر)
        works_data = [
            {'poet': poet_objs['hafez'], 'title': 'دیوان حافظ', 'slug': 'divan-hafez', 'work_type': 'دیوان'},
            {'poet': poet_objs['saadi'], 'title': 'غزلیات سعدی', 'slug': 'ghazaliat-saadi', 'work_type': 'دیوان'},
            {'poet': poet_objs['saadi'], 'title': 'بوستان سعدی', 'slug': 'bustan-saadi', 'work_type': 'مثنوی'},
            {'poet': poet_objs['saadi'], 'title': 'گلستان سعدی', 'slug': 'golestan-saadi', 'work_type': 'نثر و شعر'},
            {'poet': poet_objs['rumi'], 'title': 'غزلیات شمس تبریزی', 'slug': 'divan-shams', 'work_type': 'دیوان'},
            {'poet': poet_objs['rumi'], 'title': 'مثنوی معنوی', 'slug': 'masnavi-manavi', 'work_type': 'مثنوی'},
            {'poet': poet_objs['ferdowsi'], 'title': 'شاهنامه', 'slug': 'shahnameh', 'work_type': 'حماسی'},
            {'poet': poet_objs['khayyam'], 'title': 'رباعیات خیام', 'slug': 'robaeyat-khayyam', 'work_type': 'رباعیات'},
            {'poet': poet_objs['nezami'], 'title': 'مخزن الاسرار', 'slug': 'makhzan-al-asrar', 'work_type': 'مثنوی'},
            {'poet': poet_objs['nezami'], 'title': 'خسرو و شیرین', 'slug': 'khosrow-shirin', 'work_type': 'منظومه غنایی'},
        ]
        work_objs = {}
        for w in works_data:
            obj, _ = Work.objects.get_or_create(
                poet=w['poet'],
                slug=w['slug'],
                defaults={'title': w['title'], 'work_type': w['work_type']}
            )
            work_objs[w['slug']] = obj

        # 4. Poems & Verses (اشعار و ابیات دقیق)
        poems_data = [
            # HAFEZ 1
            {
                'poet': poet_objs['hafez'],
                'work': work_objs['divan-hafez'],
                'rhythm': rhythm_objs['فاعلاتن فعلاتن فعلاتن فعلن'],
                'title': 'الا یا ایها الساقی ادر کأسا و ناولها',
                'slug': 'ala-ya-ayyohas-saghi',
                'poem_type': Poem.PoemType.GHAZAL,
                'order_in_work': 1,
                'edition_source': 'تصحیح علامه محمد قزوینی و دکتر قاسم غنی',
                'verses': [
                    ('الا یا ایها الساقی ادر کأسا و ناولها', 'که عشق آسان نمود اول ولی افتاد مشکل‌ها'),
                    ('به بوی نافه‌ای کاخر صبا زان طره بگشاید', 'ز تاب جعد مشکینش چه خون افتاد در دل‌ها'),
                    ('مرا در منزل جانان چه امن عیش چون هر دم', 'جرس فریاد می‌دارد که بربندید محمل‌ها'),
                    ('به می سجاده رنگین کن گرت پیر مغان گوید', 'که سالک بی‌خبر نبود ز راه و رسم منزل‌ها'),
                    ('شب تاریک و بیم موج و گردابی چنین هایل', 'کجا دانند حال ما سبکباران ساحل‌ها'),
                    ('همه کارم ز خودکامی به بدنامی کشید آخر', 'نهان کی ماند آن رازی کز او سازند محفل‌ها'),
                    ('حضوری گر همی‌خواهی از او غایب مشو حافظ', 'متی ما تلق من تهوی دع الدنیا و اهملها'),
                ]
            },
            # HAFEZ 2
            {
                'poet': poet_objs['hafez'],
                'work': work_objs['divan-hafez'],
                'rhythm': rhythm_objs['فاعلاتن فعلاتن فعلاتن فعلن'],
                'title': 'صلاح کار کجا و من خراب کجا',
                'slug': 'salah-kar-koja',
                'poem_type': Poem.PoemType.GHAZAL,
                'order_in_work': 2,
                'edition_source': 'تصحیح علامه محمد قزوینی و دکتر قاسم غنی',
                'verses': [
                    ('صلاح کار کجا و من خراب کجا', 'ببین تفاوت ره از کجاست تا به کجا'),
                    ('دلم ز صومعه بگرفت و خرقه سالوس', 'کجاست دیر مغان و شراب ناب کجا'),
                    ('چه نسبت است به رندی صلاح و تقوا را', 'سماع وعظ کجا نغمه رباب کجا'),
                    ('ز روی دوست دل دشمنان چه دریابد', 'چراغ مرده کجا شمع آفتاب کجا'),
                    ('چو کحل بینش ما خاک آستان شماست', 'کجا رویم بفرما از این جناب کجا'),
                    ('قرار و خواب ز حافظ طمع مدار ای دوست', 'قرار چیست صبوری کدام و خواب کجا'),
                ]
            },
            # HAFEZ 3
            {
                'poet': poet_objs['hafez'],
                'work': work_objs['divan-hafez'],
                'rhythm': rhythm_objs['فاعلاتن فعلاتن فعلاتن فعلن'],
                'title': 'یوسف گمگشته بازآید به کنعان غم مخور',
                'slug': 'yousef-gomgashteh',
                'poem_type': Poem.PoemType.GHAZAL,
                'order_in_work': 255,
                'edition_source': 'تصحیح علامه محمد قزوینی و دکتر قاسم غنی',
                'verses': [
                    ('یوسف گمگشته بازآید به کنعان غم مخور', 'کلبه احزان شود روزی گلستان غم مخور'),
                    ('این دل غمدیده حالش به شود دل بد مکن', 'وین سر شوریده بازآید به سامان غم مخور'),
                    ('گر بهار عمر باشد باز بر طرف چمن', 'چتر گل در سر کشی ای مرغ خوشخوان غم مخور'),
                    ('دور گردون گر دو روزی بر مراد ما نرفت', 'دایما یک سان نباشد حال دوران غم مخور'),
                    ('هان مشو نومید چون واقف نه‌ای از سر غیب', 'باشد اندر پرده بازی‌های پنهان غم مخور'),
                    ('ای دل ار سیل فنا بنیاد هستی برکند', 'چون تو را نوح است کشتیبان ز طوفان غم مخور'),
                    ('در بیابان گر به شوق کعبه خواهی زد قدم', 'سرزنش‌ها گر کند خار مغیلان غم مخور'),
                    ('حافظا در کنج فقر و خلوت شب‌های تار', 'تا بود وردت دعا و درس قرآن غم مخور'),
                ]
            },
            # SAADI 1
            {
                'poet': poet_objs['saadi'],
                'work': work_objs['ghazaliat-saadi'],
                'rhythm': rhythm_objs['فاعلاتن فعلاتن فعلاتن فعلن'],
                'title': 'ای ساربان آهسته ران کارام جانم می‌رود',
                'slug': 'ey-sareban-ahesteh-ran',
                'poem_type': Poem.PoemType.GHAZAL,
                'order_in_work': 1,
                'edition_source': 'تصحیح استاد محمدعلی فروغی',
                'verses': [
                    ('ای ساربان آهسته ران کارام جانم می‌رود', 'وان دل که با خود داشتم با دلستانم می‌رود'),
                    ('من مانده‌ام مهجور از او بیچاره و رنجور از او', 'گویی که نیشی دور از او در استخوانم می‌رود'),
                    ('گفتم به نیرنگ و فسون پنهان کنم راز درون', 'رسوا نماید سوز دل کز پیرهن بیرون فتد'),
                    ('محمل بدار ای ساروان تندی مکن با کاروان', 'کز عشق آن سرو روان گویی روانم می‌رود'),
                    ('او می‌رود دامن‌کشان من زهر تنهایی چشان', 'دیگر مپرس از من نشان کز دل نشانم می‌رود'),
                    ('بازآی و بر چشمم نشین ای دلستان نازنین', 'کاشوب و فریاد از زمین بر آسمانم می‌رود'),
                    ('در رفتن جان از بدن گویند هر نوعی سخن', 'من خود به چشم خویشتن دیدم که جانم می‌رود'),
                    ('سعدی فغان از دست ما لایق نبود ای بی‌وفا', 'طاقت نمی‌آرم جفا کار از فغانم می‌رود'),
                ]
            },
            # SAADI 2 (بنی آدم)
            {
                'poet': poet_objs['saadi'],
                'work': work_objs['golestan-saadi'],
                'rhythm': rhythm_objs['فاعلاتن فعلاتن فعلاتن فعلن'],
                'title': 'بنی آدم اعضای یکدیگرند',
                'slug': 'bani-adam',
                'poem_type': Poem.PoemType.QATE,
                'order_in_work': 10,
                'edition_source': 'تصحیح محمدعلی فروغی',
                'verses': [
                    ('بنی آدم اعضای یکدیگرند', 'که در آفرینش ز یک گوهرند'),
                    ('چو عضوی به درد آورد روزگار', 'دگر عضوها را نماند قرار'),
                    ('تو کز محنت دیگران بی‌غمی', 'نشاید که نامت نهند آدمی'),
                ]
            },
            # SAADI 3
            {
                'poet': poet_objs['saadi'],
                'work': work_objs['ghazaliat-saadi'],
                'rhythm': rhythm_objs['مفاعیلن مفاعیلن فعولن'],
                'title': 'بگذار تا بگرییم چون ابر در بهاران',
                'slug': 'begzar-ta-begeriam',
                'poem_type': Poem.PoemType.GHAZAL,
                'order_in_work': 55,
                'edition_source': 'تصحیح محمدعلی فروغی',
                'verses': [
                    ('بگذار تا بگرییم چون ابر در بهاران', 'کز سنگ ناله خیزد روز وداع یاران'),
                    ('هر کو شراب فرقت روزی چشیده باشد', 'داند که سخت باشد قطع امیدواران'),
                    ('با ساربان بگویید احوال آب چشمم', 'تا بر شتر نبندد محمل به روز باران'),
                    ('بگذاشتند ما را در دیده آب حسرت', 'گریان چو در قیامت چشم گناهکاران'),
                    ('سعدی به روزگاران مهری نشسته در دل', 'بیرون نمی‌توان کرد الا به روزگاران'),
                ]
            },
            # RUMI 1 (نی‌نامه)
            {
                'poet': poet_objs['rumi'],
                'work': work_objs['masnavi-manavi'],
                'rhythm': rhythm_objs['فاعلاتن فاعلاتن فاعلاتن فاعلن'],
                'title': 'بشنو این نی چون شکایت می‌کند',
                'slug': 'beshno-in-ney',
                'poem_type': Poem.PoemType.MASNAVI,
                'order_in_work': 1,
                'edition_source': 'نسخه رینولد نیکلسون',
                'verses': [
                    ('بشنو این نی چون شکایت می‌کند', 'از جدایی‌ها حکایت می‌کند'),
                    ('کز نیستان تا مرا ببریده‌اند', 'در نفیرم مرد و زن نالیده‌اند'),
                    ('سینه خواهم شرحه شرحه از فراق', 'تا بگویم شرح درد اشتیاق'),
                    ('هر کسی کو دور ماند از اصل خویش', 'باز جوید روزگار وصل خویش'),
                    ('من به هر جمعیتی نالان شدم', 'جفت بدحالان و خوش‌حالان شدم'),
                    ('هر کسی از ظن خود شد یار من', 'از درون من نجست اسرار من'),
                    ('سر من از ناله من دور نیست', 'لیک چشم و گوش را آن نور نیست'),
                    ('تن ز جان و جان ز تن مستور نیست', 'لیک کس را دید جان دستور نیست'),
                    ('آتش است این بانگ نای و نیست باد', 'هر که این آتش ندارد نیست باد'),
                ]
            },
            # RUMI 2 (غزل شمس)
            {
                'poet': poet_objs['rumi'],
                'work': work_objs['divan-shams'],
                'rhythm': rhythm_objs['مفتعلن فاعلات مفتعلن فع'],
                'title': 'ای عاشقان ای عاشقان پیمانه را گم کرده‌ام',
                'slug': 'ey-asheghan',
                'poem_type': Poem.PoemType.GHAZAL,
                'order_in_work': 120,
                'edition_source': 'تصحیح بدیع‌الزمان فروزانفر',
                'verses': [
                    ('ای عاشقان ای عاشقان پیمانه را گم کرده‌ام', 'زان می که در پیمانه‌ها اندر نگنجد خورده‌ام'),
                    ('مستم ز خمر من لدن رو محتسب را غمز کن', 'پر باک باش و دم مزن کز نیک و بد بگذشته‌ام'),
                    ('امروز سرمستم از آن از خود برون جستم از آن', 'یکبارگی رستم از آن با جان جان پیوسته‌ام'),
                    ('خامش کنم خامش کنم در خم می سر خوش کنم', 'چون بوی گل پنهان شوم زان روی کز وی زاده‌ام'),
                ]
            },
            # FERDOWSI (آغاز شاهنامه)
            {
                'poet': poet_objs['ferdowsi'],
                'work': work_objs['shahnameh'],
                'rhythm': rhythm_objs['فعولن فعولن فعولن فعل'],
                'title': 'به نام خداوند جان و خرد',
                'slug': 'be-name-khodavande-jan-o-kherad',
                'poem_type': Poem.PoemType.MASNAVI,
                'order_in_work': 1,
                'edition_source': 'تصحیح جلال خالقی مطلق',
                'verses': [
                    ('به نام خداوند جان و خرد', 'کزین برتر اندیشه برنگذرد'),
                    ('خداوند نام و خداوند جای', 'خداوند روزی‌ده رهنمای'),
                    ('خداوند کیوان و گردان سپهر', 'فروزنده ماه و ناهید و مهر'),
                    ('ز نام و نشان و گمان برتر است', 'نگارنده بر شده پیکر است'),
                    ('به بینندگان آفریننده را', 'نبینی مرنجان دو بیننده را'),
                    ('نیابد بدو نیز اندیشه راه', 'که او برتر از نام و از جایگاه'),
                    ('سخن هر چه زین گوهران بگذرد', 'نیابد بدو راه جان و خرد'),
                    ('توانا بود هر که دانا بود', 'ز دانش دل پیر برنا بود'),
                ]
            },
            # FERDOWSI 2 (چو ایران نباشد)
            {
                'poet': poet_objs['ferdowsi'],
                'work': work_objs['shahnameh'],
                'rhythm': rhythm_objs['فعولن فعولن فعولن فعل'],
                'title': 'چو ایران نباشد تن من مباد',
                'slug': 'cho-iran-nabashad',
                'poem_type': Poem.PoemType.MASNAVI,
                'order_in_work': 450,
                'edition_source': 'تصحیح جلال خالقی مطلق',
                'verses': [
                    ('چو ایران نباشد تن من مباد', 'بدین بوم و بر زنده یک تن مباد'),
                    ('بیا تا همه تن به کشتن دهیم', 'مبادا که کشور به دشمن دهیم'),
                    ('دریغ است ایران که ویران شود', 'کنام پلنگان و شیران شود'),
                    ('همه سر به سر تن به کشتن دهیم', 'از آن به که کشور به دشمن دهیم'),
                ]
            },
            # KHAYYAM 1
            {
                'poet': poet_objs['khayyam'],
                'work': work_objs['robaeyat-khayyam'],
                'rhythm': rhythm_objs['مفعول مفاعیل مفاعیل فعل'],
                'title': 'ابر آمد و زار بر سر سبزه گریست',
                'slug': 'abr-amad-o-zar',
                'poem_type': Poem.PoemType.ROBAEI,
                'order_in_work': 1,
                'edition_source': 'گزیده صادق هدایت و محمدعلی فروغی',
                'verses': [
                    ('ابر آمد و زار بر سر سبزه گریست', 'بی باده گلرنگ نمی‌شاید زیست'),
                    ('این سبزه که امروز تماشاگه ماست', 'تا سبزه خاک ما تماشاگه کیست'),
                ]
            },
            # KHAYYAM 2
            {
                'poet': poet_objs['khayyam'],
                'work': work_objs['robaeyat-khayyam'],
                'rhythm': rhythm_objs['مفعول مفاعیل مفاعیل فعل'],
                'title': 'اسرار ازل را نه تو دانی و نه من',
                'slug': 'asrar-azal',
                'poem_type': Poem.PoemType.ROBAEI,
                'order_in_work': 2,
                'edition_source': 'گزیده صادق هدایت و محمدعلی فروغی',
                'verses': [
                    ('اسرار ازل را نه تو دانی و نه من', 'وین حرف معما نه تو خوانی و نه من'),
                    ('هست از پس پرده گفت‌وگوی من و تو', 'چون پرده برافتد نه تو مانی و نه من'),
                ]
            },
            # NEZAMI 1 (آغاز مخزن الاسرار)
            {
                'poet': poet_objs['nezami'],
                'work': work_objs['makhzan-al-asrar'],
                'rhythm': rhythm_objs['مفتعلن فاعلات مفتعلن فع'],
                'title': 'ای نام تو بهترین سرآغاز',
                'slug': 'ey-name-to-behtarin-saraghaz',
                'poem_type': Poem.PoemType.MASNAVI,
                'order_in_work': 1,
                'edition_source': 'تصحیح وحید دستگردی',
                'verses': [
                    ('ای نام تو بهترین سرآغاز', 'بی نام تو نامه کی کنم باز'),
                    ('ای یاد تو مونس روانم', 'جز نام تو نیست بر زبانم'),
                    ('ای کارگشای هر چه هستند', 'نام تو کلید هر چه بستند'),
                    ('ای هیچ نه پیش از تو بوده', 'پیدا شده و نهفته هر دو'),
                    ('پرورده به رحمتت جهانی', 'روزی‌ده بنده هر زمانی'),
                ]
            }
        ]

        total_poems = 0
        total_verses = 0

        for p_data in poems_data:
            poem, created = Poem.objects.get_or_create(
                slug=p_data['slug'],
                defaults={
                    'poet': p_data['poet'],
                    'work': p_data['work'],
                    'rhythm': p_data['rhythm'],
                    'title': p_data['title'],
                    'poem_type': p_data['poem_type'],
                    'order_in_work': p_data['order_in_work'],
                    'edition_source': p_data['edition_source'],
                }
            )
            total_poems += 1
            for order, (first, second) in enumerate(p_data['verses'], start=1):
                Verse.objects.get_or_create(
                    poem=poem,
                    order=order,
                    defaults={
                        'first_couplet': first,
                        'second_couplet': second
                    }
                )
                total_verses += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded! {len(poet_objs)} poets, {len(rhythm_objs)} rhythms, {total_poems} poems, {total_verses} verses."
        ))
