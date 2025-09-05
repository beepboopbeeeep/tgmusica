# ساختار پروژه

```
telegram_music_bot/
├── README.md                           # مستندات اصلی پروژه
├── requirements.txt                    # پکیج‌های مورد نیاز
├── setup.sh                           # اسکریپت نصب و راه‌اندازی
├── start_bot.sh                       # اسکریپت اجرای ربات
├── wsgi_config.py                     # تنظیمات WSGI برای PythonAnywhere
├── run_bot.sh                         # اسکریپت اجرا روی PythonAnywhere
├── PYTHONANYWHERE_DEPLOYMENT.md       # راهنمای راه‌اندازی روی PythonAnywhere
│
├── config/                            # پوشه تنظیمات
│   └── config.py                      # فایل تنظیمات اصلی
│
├── src/                               # پوشه سورس کد
│   ├── main.py                        # فایل اصلی ربات
│   ├── main_optimized.py              # نسخه بهینه‌شده برای PythonAnywhere
│   └── pythonanywhere_optimization.py # بهینه‌سازی‌های PythonAnywhere
│
├── downloads/                         # پوشه دانلود فایل‌ها
│   (پس از اجرای ربات ایجاد می‌شود)
│
└── logs/                              # پوشه لاگ‌ها
    (پس از اجرای ربات ایجاد می‌شود)
```

## 📁 توضیح فایل‌ها

### فایل‌های اصلی
- **README.md**: مستندات کامل پروژه و نحوه استفاده
- **requirements.txt**: لیست پکیج‌های پایتون مورد نیاز
- **setup.sh**: اسکریپت خودکار برای نصب و پیکربندی اولیه

### فایل‌های اجرایی
- **start_bot.sh**: اسکریپت ساده برای اجرای محلی ربات
- **run_bot.sh**: اسکریپت پیشرفته برای اجرا روی PythonAnywhere
- **wsgi_config.py**: تنظیمات وب اپلیکیشن برای PythonAnywhere

### پوشه تنظیمات
- **config/config.py**: تمام تنظیمات ربات including توکن، زبان‌ها، پیام‌ها

### پوشه سورس
- **src/main.py**: نسخه استاندارد ربات برای اجرای محلی
- **src/main_optimized.py**: نسخه بهینه‌شده برای PythonAnywhere
- **src/pythonanywhere_optimization.py**: توابع بهینه‌سازی برای PythonAnywhere

### پوشه‌های پویا
- **downloads/**: فایل‌های موقت دانلود شده (پس از اجرا ایجاد می‌شود)
- **logs/**: لاگ‌های اجرای ربات (پس از اجرا ایجاد می‌شود)

## 🚀 نحوه اجرا

### اجرای محلی
```bash
# 1. نصب پیش‌نیازها
pip install -r requirements.txt

# 2. پیکربندی
./setup.sh

# 3. اجرا
./start_bot.sh
```

### اجرا روی PythonAnywhere
```bash
# 1. آپلود فایل‌ها به PythonAnywhere
# 2. تنظیم فایل‌ها (جایگزینی نام کاربری)
# 3. ایجاد virtual environment
python3.8 -m venv .virtualenvs/telegram_music_bot
source .virtualenvs/telegram_music_bot/bin/activate

# 4. نصب پکیج‌ها
pip install -r requirements.txt

# 5. پیکربندی
./setup.sh

# 6. اجرا
./run_bot.sh start
```

## ⚙️ تنظیمات کلیدی

### در فایل config/config.py:
```python
# تنظیمات ربات
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
BOT_USERNAME = "YourMusicBot"
ADMIN_USER_ID = 123456789

# تنظیمات دانلود
DOWNLOAD_PATH = "./downloads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# تنظیمات زبان
DEFAULT_LANGUAGE = "fa"  # fa یا en

# تنظیمات اختیاری Spotify
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
```

## 🔧 ویژگی‌های فنی

### بهینه‌سازی‌های PythonAnywhere
- مدیریت حافظه بهینه
- کنترل خطاهای شبکه
- پاکسازی خودکار فایل‌ها
- لاگ‌ینگ پیشرفته
- health check خودکار

### پشتیبانی از پلتفرم‌ها
- YouTube (یوتیوب)
- Instagram (اینستاگرام)
- TikTok (تیک‌تاک)
- Pinterest (پینترست)
- SoundCloud (ساندکلاد)

### قابلیت‌های ربات
- تشخیص آهنگ با ShazamIO
- جستجوی اینلاین
- پشتیبانی چندزبانه
- دانلود از لینک
- ویرایش اطلاعات آهنگ

## 📊 منابع استفاده شده

### پکیج‌های اصلی
- `python-telegram-bot`: فریمورک ربات تلگرام
- `shazamio`: تشخیص آهنگ
- `yt-dlp`: دانلود از یوتیوب و پلتفرم‌ها
- `spotipy`: (اختیاری) دسترسی به Spotify API
- `requests`: درخواست‌های HTTP
- `beautifulsoup4`: پارس کردن HTML

### پکیج‌های بهینه‌سازی
- `psutil`: مانیتورینگ سیستم
- `uvloop`: حلقه رویداد بهینه
- `asyncio`: برنامه‌نویسی ناهمزمان

## 🛡️ ملاحظات امنیتی

- توکن ربات در کد ذخیره می‌شود (درخواست کاربر)
- فایل‌های موقت به‌طور خودکار پاک می‌شوند
- لاگ‌ها حاوی اطلاعات حساس نیستند
- دسترسی‌ها به حداقل محدود شده‌اند

## 📈 عملکرد

### محدودیت‌های PythonAnywhere رایگان
- حافظه: 512MB
- پردازنده: محدود
- پهنای باند: محدود
- زمان اجرا: محدود

### بهینه‌سازی‌های انجام شده
- استفاده از async/await برای عملیات I/O
- پاکسازی خودکار حافظه
- محدودیت اندازه فایل‌ها
- مدیریت خطاها و retry logic

## 🔄 بروزرسانی

برای بروزرسانی ربات:
```bash
git pull origin main
pip install -r requirements.txt
./setup.sh
```

## 🐞 عیب‌یابی

### لاگ‌ها
- `logs/bot.log`: لاگ‌های اصلی ربات
- `logs/telegram_music_bot.log`: لاگ‌های PythonAnywhere

### دستورات مفید
```bash
# بررسی سلامت
./run_bot.sh health

# پاکسازی فایل‌ها
./run_bot.sh cleanup

# راه‌اندازی مجدد
./run_bot.sh restart
```

این ساختار پروژه به گونه‌ای طراحی شده که هم برای اجرای محلی و هم برای استقرار روی PythonAnywhere مناسب باشد.