"""
Configuration file for Telegram Music Bot
All variables are defined here as requested (not in .env format)
"""

# Bot Configuration
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # Replace with your actual bot token
BOT_USERNAME = "YourMusicBot"  # Replace with your bot username

# Admin Configuration
ADMIN_USER_ID = 123456789  # Replace with your admin user ID

# Download Configuration
DOWNLOAD_PATH = "./downloads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB Telegram limit

# ShazamIO Configuration
SHAZAM_TIMEOUT = 30  # seconds

# Language Configuration
DEFAULT_LANGUAGE = "fa"  # fa for Persian, en for English

# Social Media Download Configuration
YOUTUBE_DL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': True,
    'no_warnings': True,
}

# Spotify Configuration (optional)
SPOTIFY_CLIENT_ID = ""  # Optional: for better music metadata
SPOTIFY_CLIENT_SECRET = ""  # Optional: for better music metadata

# Bot Messages
BOT_MESSAGES = {
    'fa': {
        'start': """
🎵 **به ربات موسیقی هوشمند خوش آمدید!**

این ربات قابلیت‌های زیر را ارائه می‌دهد:

🔍 **تشخیص آهنگ**: ارسال فایل صوتی برای تشخیص خودکار آهنگ
📥 **دانلود از پلتفرم‌ها**: دانلود موسیقی از یوتیوب، اینستاگرام، تیک‌تاک، پینترست و ساندکلاد
🎼 **جستجوی آهنگ**: جستجوی آهنگ با استفاده از اینلاین کیبورد
🏷️ **ویرایش اطلاعات**: ویرایش نام آهنگ، هنرمند و آلبوم
🌍 **چندزبانه**: پشتیبانی از فارسی و انگلیسی

برای شروع از دستورات زیر استفاده کنید:
/start - شروع ربات
/language - تغییر زبان
/help - راهنما

برای استفاده در گروه‌ها می‌توانید از @{} استفاده کنید.
        """,
        'language_select': "لطفاً زبان مورد نظر خود را انتخاب کنید:",
        'send_audio': "لطفاً یک فایل صوتی ارسال کنید تا آهنگ را تشخیص دهم:",
        'processing': "در حال پردازش... لطفاً صبر کنید",
        'song_not_found': "متأسفانه آهنگی پیدا نشد. لطفاً دوباره تلاش کنید.",
        'download_error': "خطا در دانلود فایل. لطفاً دوباره تلاش کنید.",
        'edit_info': "اطلاعات آهنگ را ویرایش کنید:",
        'send_link': "لطفاً لینک مورد نظر را ارسال کنید:",
        'invalid_link': "لینک نامعتبر است. لطفاً لینک معتبر ارسال کنید.",
        'success': "عملیات با موفقیت انجام شد!",
        'error': "خطایی رخ داد. لطفاً دوباره تلاش کنید.",
    },
    'en': {
        'start': """
🎵 **Welcome to the Smart Music Bot!**

This bot provides the following features:

🔍 **Song Recognition**: Send audio file to automatically recognize the song
📥 **Download from Platforms**: Download music from YouTube, Instagram, TikTok, Pinterest, and SoundCloud
🎼 **Song Search**: Search songs using inline keyboard
🏷️ **Edit Info**: Edit song title, artist, and album
🌍 **Multi-language**: Support for Persian and English

Use the following commands to start:
/start - Start the bot
/language - Change language
/help - Help

For use in groups, you can use @{}
        """,
        'language_select': "Please select your preferred language:",
        'send_audio': "Please send an audio file to recognize the song:",
        'processing': "Processing... Please wait",
        'song_not_found': "Unfortunately, no song was found. Please try again.",
        'download_error': "Error downloading file. Please try again.",
        'edit_info': "Edit song information:",
        'send_link': "Please send the desired link:",
        'invalid_link': "Invalid link. Please send a valid link.",
        'success': "Operation completed successfully!",
        'error': "An error occurred. Please try again.",
    }
}

# Supported Platforms for Download
SUPPORTED_PLATFORMS = {
    'youtube': ['youtube.com', 'youtu.be', 'music.youtube.com'],
    'instagram': ['instagram.com', 'www.instagram.com'],
    'tiktok': ['tiktok.com', 'www.tiktok.com'],
    'pinterest': ['pinterest.com', 'www.pinterest.com'],
    'soundcloud': ['soundcloud.com', 'www.soundcloud.com']
}

# Button Texts
BUTTON_TEXTS = {
    'fa': {
        'persian': 'فارسی 🇮🇷',
        'english': 'English 🇺🇸',
        'edit_info': 'ویرایش اطلاعات آهنگ',
        'download_from_link': 'دانلود از لینک',
        'back': 'بازگشت',
        'cancel': 'لغو',
    },
    'en': {
        'persian': 'فارسی 🇮🇷',
        'english': 'English 🇺🇸',
        'edit_info': 'Edit Song Info',
        'download_from_link': 'Download from Link',
        'back': 'Back',
        'cancel': 'Cancel',
    }
}