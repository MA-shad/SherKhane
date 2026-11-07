# نمودار جامع ارتباط موجودیت‌ها (Database ERD)

این سند، دیاگرام ارتباط میان موجودیت‌های داده‌ای سامانه شعرخونه را با نمادگذاری استاندارد ارائه می‌کند.

---

## ۱. نمودار روابط موجودیت‌ها

```mermaid
erDiagram
    USER ||--o{ USER_PROFILE : "دارد"
    USER ||--o{ USER_BOOKMARK : "ذخیره می‌کند"
    USER ||--o{ MEMORIZATION_ITEM : "در حافظه دارد"
    USER ||--o{ GAME_SESSION : "شرکت می‌کند"
    USER ||--o{ ACHIEVEMENT_EARNED : "کسب کرده"

    POET ||--o{ WORK : "سروده است"
    WORK ||--o{ POEM : "شامل می‌شود"
    RHYTHM ||--o{ POEM : "تعیین‌کننده وزن"
    POEM ||--o{ STANZA : "شامل بندها"
    STANZA ||--o{ VERSE : "شامل ابیات"
    VERSE ||--o{ HEMISTICH : "شامل مصراع‌ها"

    POEM ||--o{ USER_BOOKMARK : "نشانه‌گذاری شده در"
    POEM ||--o{ MEMORIZATION_ITEM : "تمرین شده در"

    MEMORIZATION_ITEM ||--o{ MEMORIZATION_LOG : "دارای تاریخچه مرور"
    GAME_SESSION ||--o{ GAME_TURN : "دارای نوبت‌ها"

    USER {
        bigint id PK
        string username UK
        string email
        string password
        datetime date_joined
    }

    USER_PROFILE {
        bigint id PK
        bigint user_id FK
        string display_name
        string avatar
        int xp_points
        int current_streak
        datetime last_activity
    }

    POET {
        bigint id PK
        string name UK
        string slug UK
        text bio
        int century
        string birth_place
    }

    WORK {
        bigint id PK
        bigint poet_id FK
        string title
        string slug
        string work_type
    }

    RHYTHM {
        bigint id PK
        string name UK
        string bahr
        string pattern
    }

    POEM {
        bigint id PK
        bigint work_id FK
        bigint rhythm_id FK
        string title
        string slug
        string poem_type
        int order_in_work
    }

    VERSE {
        bigint id PK
        bigint poem_id FK
        int order
        text first_couplet
        text second_couplet
        text normalized_text
    }

    USER_BOOKMARK {
        bigint id PK
        bigint user_id FK
        bigint poem_id FK
        string category_tag
        text note
        datetime created_at
    }

    MEMORIZATION_ITEM {
        bigint id PK
        bigint user_id FK
        bigint poem_id FK
        int mastery_level
        float easiness_factor
        int interval_days
        datetime next_review_date
        int repetitions
    }

    GAME_SESSION {
        bigint id PK
        bigint user_id FK
        string game_type
        int score
        int turns_count
        string status
        datetime start_time
        datetime end_time
    }
```

---

## ۲. توضیحات روابط ساختاری داده‌ها
1. **سلسله‌مراتب شعر:** هر شاعر آثاری دارد، هر اثر اشعاری دارد، و هر شعر به ابیات و مصراع‌ها با ترتیب قطعی متصل است.
2. **استودیو یادسپاری:** هر کاربر به ازای هر شعر انتخابی، یک آیتم یادسپاری فعال دارد که داده‌های ضریب آسانی و دوره تکرار را نگهداری می‌کند.
3. **دفترچه شخصی:** کاربر می‌تواند اشعار دلخواه را با برچسب‌های دلخواه و یادداشت شخصی نشانه‌گذاری کند.
4. **نشست‌های بازی:** هر دست بازی یا مشاعره به عنوان یک نشست مستقل همراه با امتیاز و تاریخچه نوبت‌ها ثبت می‌شود.
