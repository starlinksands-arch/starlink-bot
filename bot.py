import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler
from datetime import time
import pytz

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⭐ YOUR BOT CONFIGURATION ⭐
BOT_TOKEN = "8980129391:AAGBpDB65FpClgm7HbosFO_PEMo5zt68_HA"

# All 8 Admin Groups
ADMIN_GROUP_IDS = [
    -1001930066266,
    -1001539099161,
    -1001902362425,
    -1001860892615,
    -1001605945325,
    -1001871789690,
    -1001882585760,
    -1001504806616,
]

TARGET_GROUP_LINK = "https://t.me/StarlinkGamesEN"
CHANNEL_LINK = "https://t.me/starlinkchannel"
PHOTO_URL = "https://ibb.co/bp478pt"

# Philippines timezone
PH_TZ = pytz.timezone('Asia/Manila')

def get_invite_buttons():
    """Create clickable buttons for group and channel"""
    keyboard = [
        [
            InlineKeyboardButton("👥 Join Group", url=TARGET_GROUP_LINK),
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when /start command is issued"""
    caption = (
        "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
        "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
        "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️"
    )
    await update.message.reply_text(caption, reply_markup=get_invite_buttons())

async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send invite link with photo when user requests it with /invite"""
    caption = (
        "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
        "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
        "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️"
    )
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=caption,
        reply_markup=get_invite_buttons()
    )

async def member_joined(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Automatically send invite with photo when someone joins any of the admin groups"""
    if update.message.chat_id not in ADMIN_GROUP_IDS:
        return
    
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.is_bot:
                continue
            
            caption = (
                f"👋 Welcome, {member.mention_html()}!\n\n"
                "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
                "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
                "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️"
            )
            
            await update.message.reply_photo(
                photo=PHOTO_URL,
                caption=caption,
                reply_markup=get_invite_buttons(),
                parse_mode='HTML'
            )
            logger.info(f"✅ Sent invite to {member.username or member.first_name}")

async def daily_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send daily reminder at 8 PM Philippines time"""
    caption = (
        "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
        "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
        "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️"
    )
    
    for group_id in ADMIN_GROUP_IDS:
        try:
            await context.bot.send_photo(
                chat_id=group_id,
                photo=PHOTO_URL,
                caption=caption,
                reply_markup=get_invite_buttons()
            )
            logger.info(f"✅ Sent daily reminder to group {group_id}")
        except Exception as e:
            logger.error(f"❌ Failed to send reminder: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

async def main() -> None:
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("invite", invite_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, member_joined))
    application.add_error_handler(error_handler)
    
    # Schedule daily reminder at 8 PM PH time
    job_queue = application.job_queue
    job_queue.run_daily(
        daily_reminder,
        time=time(20, 0, 0, tzinfo=PH_TZ),
        name='daily_reminder'
    )
    
    print("🤖 Bot is running! Daily reminder at 8 PM Philippines time")
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
