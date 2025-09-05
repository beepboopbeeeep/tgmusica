# راهنمای راه‌اندازی ربات تلگرامی موسیقی روی PythonAnywhere

این راهنما به شما نشان می‌دهد که چگونه ربات تلگرامی موسیقی را روی PythonAnywhere راه‌اندازی کنید.

## 📋 پیش‌نیازها

1. **حساب PythonAnywhere**
   - یک حساب رایگان یا پولی روی PythonAnywhere
   - دسترسی به کنسول bash

2. **ربات تلگرام**
   - توکن ربات تلگرام (از @BotFather)
   - نام کاربری ربات

3. **دانش فنی**
   - آشنایی با دستورات لینوکس
   - آشنایی با Git

## 🚀 مراحل راه‌اندازی

### مرحله ۱: آماده‌سازی محیط

1. **وارد حساب PythonAnywhere خود شوید**
   - به [pythonanywhere.com](https://www.pythonanywhere.com) بروید
   - وارد حساب کاربری خود شوید

2. **به کنسول بروید**
   - از منوی بالا، **"Consoles"** را انتخاب کنید
   - روی **"Start a new console"** کلیک کنید
   - **"Bash"** را انتخاب کنید

### مرحله ۲: دانلود و آماده‌سازی پروژه

1. **دانلود پروژه**
```bash
cd /home/your_username
git clone https://github.com/yourusername/telegram-music-bot.git
cd telegram-music-bot
```

**توجه**: `your_username` را با نام کاربری واقعی خود در PythonAnywhere جایگزین کنید.

2. **بهینه‌سازی فایل‌ها برای PythonAnywhere**
```bash
# ویرایش فایل wsgi_config.py
nano wsgi_config.py
```

در فایل `wsgi_config.py`، خط زیر را پیدا کرده و نام کاربری خود را جایگزین کنید:
```python
project_home = '/home/your_username/telegram_music_bot'  # Replace with your username
```

3. **ویرایش فایل run_bot.sh**
```bash
nano run_bot.sh
```

در فایل `run_bot.sh`، متغیر زیر را ویرایش کنید:
```bash
PYTHONANYWHERE_USERNAME="your_username"  # Replace with your actual username
```

### مرحله ۳: ایجاد محیط مجازی (Virtual Environment)

1. **ایجاد virtual environment**
```bash
cd /home/your_username
python3.8 -m venv .virtualenvs/telegram_music_bot
source .virtualenvs/telegram_music_bot/bin/activate
```

2. **نصب پکیج‌های مورد نیاز**
```bash
cd /home/your_username/telegram_music_bot
pip install --upgrade pip
pip install -r requirements.txt
```

### مرحله ۴: پیکربندی ربات

1. **اجرای اسکریپت تنظیمات**
```bash
chmod +x setup.sh
./setup.sh
```

2. **وارد کردن اطلاعات**
   - توکن ربات تلگرام خود را وارد کنید
   - نام کاربری ربات را وارد کنید
   - شناسه کاربری ادمین را وارد کنید
   - (اختیاری) اطلاعات Spotify را وارد کنید

### مرحله ۵: تست ربات

1. **تست اجرای ربات**
```bash
cd /home/your_username/telegram_music_bot
source /home/your_username/.virtualenvs/telegram_music_bot/bin/activate
python src/main_optimized.py
```

اگر ربات بدون خطا اجرا شد، با `Ctrl+C` آن را متوقف کنید.

### مرحله ۶: ایجاد Task برای اجرای خودکار

1. **به بخش Tasks بروید**
   - از منوی بالا، **"Tasks"** را انتخاب کنید

2. **ایجاد Task جدید**
   - روی **"Create a new task"** کلیک کنید
   - تنظیمات زیر را وارد کنید:

   **Description**: `Telegram Music Bot`
   
   **Command**: 
   ```
   /home/your_username/telegram_music_bot/run_bot.sh start
   ```
   
   **Timeout**: `24 hours`
   
   **Hour**: `*`
   
   **Minute**: `*/5`
   
   **Day of week**: `*`

3. **ذخیره Task**
   - روی **"Create"** کلیک کنید

### مرحله ۷: راه‌اندازی Web App (اختیاری)

برای داشتن یک وب اپلیکیشن برای مانیتورینگ:

1. **به بخش Web بروید**
   - از منوی بالا، **"Web"** را انتخاب کنید

2. **ایجاد Web App جدید**
   - روی **"Add a new web app"** کلیک کنید
   - **"Python"** را انتخاب کنید
   - **"Python 3.8"** را انتخاب کنید
   - مسیر پروژه را وارد کنید: `/home/your_username/telegram_music_bot`

3. **پیکربندی WSGI**
   - در بخش **"WSGI configuration file"**، مسیر زیر را وارد کنید:
   ```
   /home/your_username/telegram_music_bot/wsgi_config.py
   ```

4. **ذخیره و راه‌اندازی**
   - روی **"Save"** کلیک کنید
   - سپس روی **"Reload"** کلیک کنید

## 🔧 عیب‌یابی و مشکلات رایج

### مشکل ۱: خطای "Module not found"
**راه‌حل**:
```bash
source /home/your_username/.virtualenvs/telegram_music_bot/bin/activate
pip install -r requirements.txt
```

### مشکل ۲: خطای "Permission denied"
**راه‌حل**:
```bash
chmod +x setup.sh
chmod +x run_bot.sh
chmod +x start_bot.sh
```

### مشکل ۳: ربات پاسخ نمی‌دهد
**راه‌حل**:
1. لاگ‌ها را بررسی کنید:
```bash
tail -f /home/your_username/logs/telegram_music_bot.log
```

2. Task را ری‌استارت کنید:
   - به بخش **"Tasks"** بروید
   - Task را غیرفعال و دوباره فعال کنید

### مشکل ۴: خطای حافظه (Memory Error)
**راه‌حل**:
PythonAnywhere رایگان محدودیت حافظه دارد. برای کاهش مصرف حافظه:

1. فایل‌های قدیمی را پاک کنید:
```bash
/home/your_username/telegram_music_bot/run_bot.sh cleanup
```

2. از نسخه بهینه‌شده استفاده کنید:
```bash
python src/main_optimized.py
```

### مشکل ۵: خطای شبکه
**راه‌حل**:
1. اتصال اینترنت را بررسی کنید
2. فایروال PythonAnywhere را بررسی کنید
3. از VPN استفاده نکنید

## 📊 مانیتورینگ و نگهداری

### بررسی لاگ‌ها
```bash
# مشاهده لاگ‌های ربات
tail -f /home/your_username/logs/telegram_music_bot.log

# مشاهده لاگ‌های سیستم
tail -f /var/log/apache2/error.log
```

### بررسی وضعیت ربات
```bash
# بررسی سلامت ربات
/home/your_username/telegram_music_bot/run_bot.sh health

# بررسی وضعیت پردازش
ps aux | grep python
```

### به‌روزرسانی ربات
```bash
cd /home/your_username/telegram_music_bot
git pull origin main
source /home/your_username/.virtualenvs/telegram_music_bot/bin/activate
pip install -r requirements.txt
```

### پشتیبان‌گیری
```bash
# پشتیبان‌گیری از تنظیمات
cp config/config.py config/config.py.backup

# پشتیبان‌گیری از کل پروژه
tar -czf backup.tar.gz /home/your_username/telegram_music_bot
```

## 🚀 نکات بهینه‌سازی

### ۱. بهینه‌سازی حافظه
- از نسخه بهینه‌شده (`main_optimized.py`) استفاده کنید
- به‌طور منظم فایل‌های موقت را پاک کنید
- از تابع `cleanup` در اسکریپت استفاده کنید

### ۲. بهینه‌سازی شبکه
- از timeout مناسب در درخواست‌ها استفاده کنید
- از retry logic برای درخواست‌های ناموفق استفاده کنید
- کش را فعال کنید

### ۳. بهینه‌سازی پردازش
- از async/await برای عملیات I/O استفاده کنید
- از uvloop برای عملکرد بهتر استفاده کنید
- پردازش‌های سنگین را محدود کنید

### ۴. امنیت
- توکن ربات را در محیط امن نگه دارید
- لاگ‌ها را به‌طور منظم بررسی کنید
- دسترسی‌ها را محدود کنید

## 📞 پشتیبانی

اگر با مشکلی مواجه شدید:

1. **لاگ‌ها را بررسی کنید**
   - لاگ‌های ربات: `/home/your_username/logs/telegram_music_bot.log`
   - لاگ‌های سیستم: `/var/log/apache2/error.log`

2. **از دستورات عیب‌یابی استفاده کنید**
```bash
/home/your_username/telegram_music_bot/run_bot.sh health
/home/your_username/telegram_music_bot/run_bot.sh setup
```

3. **با ادمین تماس بگیرید**
   - لاگ‌های مربوطه را ارسال کنید
   - مراحل انجام شده را توضیح دهید

## 🎉 تبریک!

ربات تلگرامی موسیقی شما با موفقیت روی PythonAnywhere راه‌اندازی شد. حالا می‌توانید:

- آهنگ‌ها را با ارسال فایل صوتی تشخیص دهید
- موسیقی از پلتفرم‌های مختلف دانلود کنید
- از قابلیت‌های اینلاین در گروه‌ها استفاده کنید
- زبان ربات را تغییر دهید
- و بسیاری از قابلیت‌های دیگر...

موفق باشید! 🎵