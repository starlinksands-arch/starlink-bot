import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler

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
# Your Starlink photo
PHOTO_URL = "https://ibb.co/bp478pt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when /start command is issued"""
    await update.message.reply_text(
        "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
        "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
        "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️\n\n"
        f"👥 Group: {TARGET_GROUP_LINK}\n"
        f"📢 Channel: {CHANNEL_LINK}"
    )

async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send invite link with photo when user requests it with /invite"""
    caption = (
        "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
        "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
        "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️\n\n"
        f"👥 Group: {TARGET_GROUP_LINK}\n"
        f"📢 Channel: {CHANNEL_LINK}"
    )
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=caption,
        parse_mode='HTML'
    )

async def member_joined(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Automatically send invite with photo when someone joins any of the admin groups"""
    # Check if this is one of our admin groups
    if update.message.chat_id not in ADMIN_GROUP_IDS:
        return
    
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            # Skip if it's the bot itself
            if member.is_bot:
                continue
            
            # Send welcome message with photo and invite link
            caption = (
                f"👋 Welcome, {member.mention_html()}!\n\n"
                "🚀 GRAND OPENING COMING SOON! 🎉\n\n"
                "🎁 Join BOTH our Telegram Group & Channel now to receive FREE Grand Opening Rewards!\n\n"
                "⚠️ Rewards are available to Group & Channel Members ONLY. ⚠️\n\n"
                f"👥 Group: {TARGET_GROUP_LINK}\n"
                f"📢 Channel: {CHANNEL_LINK}"
            )
            
            await update.message.reply_photo(
                photo=PHOTO_URL,
                caption=caption,
                parse_mode='HTML'
            )
            logger.info(f"✅ Sent invite with photo to {member.username or member.first_name} in group {update.message.chat_id}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("invite", invite_command))
    
    # Add handler for new members
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, member_joined))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    print("🤖 Bot is running in 8 admin groups! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()
