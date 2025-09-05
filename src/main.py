"""
Main Telegram Music Bot
Features: Song recognition, download from platforms, multi-language support, inline search
"""

import asyncio
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Dict, Optional, List, Any

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    Message,
    BotCommand,
    InlineQueryResultAudio,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
    CallbackContext,
)
from telegram.error import TelegramError

from shazamio import Shazam
import yt_dlp
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Import configuration
from config.config import *

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure directories exist
Path(DOWNLOAD_PATH).mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)

# Conversation states
EDIT_TITLE, EDIT_ARTIST, EDIT_ALBUM = range(3)
DOWNLOAD_LINK = range(1)

# User language storage
user_languages: Dict[int, str] = {}

class MusicBot:
    def __init__(self):
        self.shazam = Shazam()
        self.spotify = None
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            try:
                auth_manager = SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET
                )
                self.spotify = spotipy.Spotify(auth_manager=auth_manager)
            except Exception as e:
                logger.error(f"Failed to initialize Spotify: {e}")

    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        return user_languages.get(user_id, DEFAULT_LANGUAGE)

    def get_message(self, user_id: int, key: str) -> str:
        """Get localized message"""
        lang = self.get_user_language(user_id)
        return BOT_MESSAGES[lang].get(key, key)

    def get_button_text(self, user_id: int, key: str) -> str:
        """Get localized button text"""
        lang = self.get_user_language(user_id)
        return BUTTON_TEXTS[lang].get(key, key)

    async def recognize_song(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Recognize song using ShazamIO"""
        try:
            result = await self.shazam.recognize(file_path)
            if result and result.get('track'):
                return result['track']
        except Exception as e:
            logger.error(f"Error recognizing song: {e}")
        return None

    def detect_platform(self, url: str) -> Optional[str]:
        """Detect which platform the URL belongs to"""
        for platform, domains in SUPPORTED_PLATFORMS.items():
            for domain in domains:
                if domain in url:
                    return platform
        return None

    async def download_from_youtube(self, url: str, video_id: str) -> Optional[str]:
        """Download audio from YouTube"""
        try:
            ydl_opts = YOUTUBE_DL_OPTIONS.copy()
            ydl_opts['outtmpl'] = f'{DOWNLOAD_PATH}/{video_id}.%(ext)s'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # Convert to mp3 if needed
                if filename.endswith('.webm') or filename.endswith('.m4a'):
                    mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
                    if os.path.exists(mp3_filename):
                        return mp3_filename
                return filename
        except Exception as e:
            logger.error(f"Error downloading from YouTube: {e}")
        return None

    async def download_from_soundcloud(self, url: str, track_id: str) -> Optional[str]:
        """Download audio from SoundCloud"""
        try:
            ydl_opts = YOUTUBE_DL_OPTIONS.copy()
            ydl_opts['outtmpl'] = f'{DOWNLOAD_PATH}/{track_id}.%(ext)s'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            logger.error(f"Error downloading from SoundCloud: {e}")
        return None

    async def download_from_instagram(self, url: str, media_id: str) -> Optional[str]:
        """Download audio from Instagram"""
        try:
            # Use yt-dlp for Instagram as well
            ydl_opts = YOUTUBE_DL_OPTIONS.copy()
            ydl_opts['outtmpl'] = f'{DOWNLOAD_PATH}/{media_id}.%(ext)s'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            logger.error(f"Error downloading from Instagram: {e}")
        return None

    async def download_from_tiktok(self, url: str, video_id: str) -> Optional[str]:
        """Download audio from TikTok"""
        try:
            ydl_opts = YOUTUBE_DL_OPTIONS.copy()
            ydl_opts['outtmpl'] = f'{DOWNLOAD_PATH}/{video_id}.%(ext)s'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            logger.error(f"Error downloading from TikTok: {e}")
        return None

    async def download_from_pinterest(self, url: str, pin_id: str) -> Optional[str]:
        """Download audio from Pinterest"""
        try:
            ydl_opts = YOUTUBE_DL_OPTIONS.copy()
            ydl_opts['outtmpl'] = f'{DOWNLOAD_PATH}/{pin_id}.%(ext)s'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            logger.error(f"Error downloading from Pinterest: {e}")
        return None

    async def download_audio(self, url: str) -> Optional[str]:
        """Download audio from various platforms"""
        platform = self.detect_platform(url)
        if not platform:
            return None

        # Generate a unique ID for the file
        file_id = re.sub(r'[^\w\-_\.]', '_', url)[:50]
        
        if platform == 'youtube':
            return await self.download_from_youtube(url, file_id)
        elif platform == 'soundcloud':
            return await self.download_from_soundcloud(url, file_id)
        elif platform == 'instagram':
            return await self.download_from_instagram(url, file_id)
        elif platform == 'tiktok':
            return await self.download_from_tiktok(url, file_id)
        elif platform == 'pinterest':
            return await self.download_from_pinterest(url, file_id)
        
        return None

    async def search_song(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for songs using Shazam"""
        try:
            results = await self.shazam.search_track(query=query, limit=limit)
            if results and results.get('tracks', {}).get('hits'):
                return results['tracks']['hits']
        except Exception as e:
            logger.error(f"Error searching songs: {e}")
        return []

    def format_song_info(self, track: Dict[str, Any]) -> str:
        """Format song information for display"""
        title = track.get('title', 'Unknown')
        artist = track.get('subtitle', 'Unknown Artist')
        album = track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'Unknown Album')
        
        return f"🎵 {title}\n👤 {artist}\n💿 {album}"

    def clean_old_files(self):
        """Clean old downloaded files"""
        try:
            for file in Path(DOWNLOAD_PATH).glob('*'):
                if file.is_file():
                    file.unlink()
        except Exception as e:
            logger.error(f"Error cleaning old files: {e}")

# Create bot instance
bot = MusicBot()

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    user_languages[user_id] = DEFAULT_LANGUAGE
    
    welcome_text = bot.get_message(user_id, 'start').format(BOT_USERNAME)
    
    keyboard = [
        [
            InlineKeyboardButton(bot.get_button_text(user_id, 'persian'), callback_data='lang_fa'),
            InlineKeyboardButton(bot.get_button_text(user_id, 'english'), callback_data='lang_en'),
        ],
        [
            InlineKeyboardButton(bot.get_button_text(user_id, 'edit_info'), callback_data='edit_info'),
            InlineKeyboardButton(bot.get_button_text(user_id, 'download_from_link'), callback_data='download_link'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_id = update.effective_user.id
    help_text = bot.get_message(user_id, 'start').format(BOT_USERNAME)
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /language command"""
    user_id = update.effective_user.id
    
    keyboard = [
        [
            InlineKeyboardButton(bot.get_button_text(user_id, 'persian'), callback_data='lang_fa'),
            InlineKeyboardButton(bot.get_button_text(user_id, 'english'), callback_data='lang_en'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        bot.get_message(user_id, 'language_select'),
        reply_markup=reply_markup
    )

# Message handlers
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle audio messages"""
    user_id = update.effective_user.id
    
    # Send processing message
    processing_msg = await update.message.reply_text(bot.get_message(user_id, 'processing'))
    
    try:
        # Download audio file
        audio_file = await update.message.audio.get_file()
        file_path = f"{DOWNLOAD_PATH}/temp_audio_{user_id}.mp3"
        await audio_file.download_to_drive(file_path)
        
        # Recognize song
        track = await bot.recognize_song(file_path)
        
        if track:
            # Format song info
            title = track.get('title', 'Unknown')
            artist = track.get('subtitle', 'Unknown Artist')
            album = track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'Unknown Album')
            
            # Try to download the song
            search_query = f"{title} {artist}"
            search_results = await bot.search_song(search_query, limit=1)
            
            if search_results:
                # For now, just send the recognized info
                info_text = f"🎵 **{title}**\n👤 **{artist}**\n💿 **{album}**\n\n✅ {bot.get_message(user_id, 'success')}"
                
                keyboard = [
                    [
                        InlineKeyboardButton(bot.get_button_text(user_id, 'edit_info'), callback_data='edit_info'),
                        InlineKeyboardButton(bot.get_button_text(user_id, 'download_from_link'), callback_data='download_link'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await processing_msg.edit_text(info_text, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                await processing_msg.edit_text(f"🎵 **{title}**\n👤 **{artist}**\n💿 **{album}**\n\n⚠️ {bot.get_message(user_id, 'song_not_found')}", parse_mode='Markdown')
        else:
            await processing_msg.edit_text(bot.get_message(user_id, 'song_not_found'))
    
    except Exception as e:
        logger.error(f"Error handling audio: {e}")
        await processing_msg.edit_text(bot.get_message(user_id, 'error'))
    
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages"""
    user_id = update.effective_user.id
    
    # Send processing message
    processing_msg = await update.message.reply_text(bot.get_message(user_id, 'processing'))
    
    try:
        # Download voice file
        voice_file = await update.message.voice.get_file()
        file_path = f"{DOWNLOAD_PATH}/temp_voice_{user_id}.ogg"
        await voice_file.download_to_drive(file_path)
        
        # Recognize song
        track = await bot.recognize_song(file_path)
        
        if track:
            # Format song info
            title = track.get('title', 'Unknown')
            artist = track.get('subtitle', 'Unknown Artist')
            album = track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'Unknown Album')
            
            info_text = f"🎵 **{title}**\n👤 **{artist}**\n💿 **{album}**\n\n✅ {bot.get_message(user_id, 'success')}"
            
            keyboard = [
                [
                    InlineKeyboardButton(bot.get_button_text(user_id, 'edit_info'), callback_data='edit_info'),
                    InlineKeyboardButton(bot.get_button_text(user_id, 'download_from_link'), callback_data='download_link'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await processing_msg.edit_text(info_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await processing_msg.edit_text(bot.get_message(user_id, 'song_not_found'))
    
    except Exception as e:
        logger.error(f"Error handling voice: {e}")
        await processing_msg.edit_text(bot.get_message(user_id, 'error'))
    
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (URLs)"""
    user_id = update.effective_user.id
    text = update.message.text
    
    # Check if it's a URL
    if re.match(r'https?://', text):
        platform = bot.detect_platform(text)
        if platform:
            # Send processing message
            processing_msg = await update.message.reply_text(bot.get_message(user_id, 'processing'))
            
            try:
                # Download audio
                file_path = await bot.download_audio(text)
                
                if file_path and os.path.exists(file_path):
                    # Try to recognize the song
                    track = await bot.recognize_song(file_path)
                    
                    if track:
                        title = track.get('title', 'Unknown')
                        artist = track.get('subtitle', 'Unknown Artist')
                        album = track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'Unknown Album')
                        
                        info_text = f"🎵 **{title}**\n👤 **{artist}**\n💿 **{album}**\n\n✅ {bot.get_message(user_id, 'success')}"
                        
                        # Send audio file
                        with open(file_path, 'rb') as audio_file:
                            await update.message.reply_audio(
                                audio=audio_file,
                                title=title,
                                performer=artist,
                                caption=info_text,
                                parse_mode='Markdown'
                            )
                    else:
                        # Just send the downloaded audio
                        with open(file_path, 'rb') as audio_file:
                            await update.message.reply_audio(
                                audio=audio_file,
                                caption=f"✅ {bot.get_message(user_id, 'success')}"
                            )
                    
                    await processing_msg.delete()
                else:
                    await processing_msg.edit_text(bot.get_message(user_id, 'download_error'))
            
            except Exception as e:
                logger.error(f"Error handling URL: {e}")
                await processing_msg.edit_text(bot.get_message(user_id, 'error'))
            
            finally:
                # Clean up
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
        else:
            await update.message.reply_text(bot.get_message(user_id, 'invalid_link'))

# Callback query handlers
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    
    await query.answer()
    
    if data.startswith('lang_'):
        # Language selection
        lang = data.split('_')[1]
        user_languages[user_id] = lang
        
        keyboard = [
            [
                InlineKeyboardButton(bot.get_button_text(user_id, 'edit_info'), callback_data='edit_info'),
                InlineKeyboardButton(bot.get_button_text(user_id, 'download_from_link'), callback_data='download_link'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"✅ {bot.get_message(user_id, 'success')}",
            reply_markup=reply_markup
        )
    
    elif data == 'edit_info':
        # Start edit info conversation
        keyboard = [
            [InlineKeyboardButton(bot.get_button_text(user_id, 'back'), callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            bot.get_message(user_id, 'edit_info'),
            reply_markup=reply_markup
        )
        # Here you would start a conversation handler for editing info
    
    elif data == 'download_link':
        # Start download from link conversation
        keyboard = [
            [InlineKeyboardButton(bot.get_button_text(user_id, 'back'), callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            bot.get_message(user_id, 'send_link'),
            reply_markup=reply_markup
        )
    
    elif data == 'back_to_main':
        # Back to main menu
        keyboard = [
            [
                InlineKeyboardButton(bot.get_button_text(user_id, 'persian'), callback_data='lang_fa'),
                InlineKeyboardButton(bot.get_button_text(user_id, 'english'), callback_data='lang_en'),
            ],
            [
                InlineKeyboardButton(bot.get_button_text(user_id, 'edit_info'), callback_data='edit_info'),
                InlineKeyboardButton(bot.get_button_text(user_id, 'download_from_link'), callback_data='download_link'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            bot.get_message(user_id, 'start').format(BOT_USERNAME),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline queries"""
    query = update.inline_query.query
    user_id = update.inline_query.from_user.id
    
    if not query:
        return
    
    try:
        # Search for songs
        results = await bot.search_song(query, limit=10)
        
        inline_results = []
        for i, hit in enumerate(results[:10]):
            track = hit.get('track', {})
            if track:
                title = track.get('title', 'Unknown')
                artist = track.get('subtitle', 'Unknown Artist')
                track_id = track.get('key', str(i))
                
                # Create inline result
                result = InlineQueryResultArticle(
                    id=track_id,
                    title=f"{title} - {artist}",
                    description=bot.format_song_info(track),
                    input_message_content=InputTextMessageContent(
                        message_text=bot.format_song_info(track),
                        parse_mode='Markdown'
                    ),
                    thumb_url=track.get('images', {}).get('coverart', '')
                )
                inline_results.append(result)
        
        await update.inline_query.answer(inline_results, cache_time=60)
    
    except Exception as e:
        logger.error(f"Error in inline query: {e}")

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

# Main function
def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Add inline query handler
    application.add_handler(InlineQueryHandler(inline_query))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Set bot commands
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help"),
        BotCommand("language", "Change language"),
    ]
    application.bot.set_my_commands(commands)
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()