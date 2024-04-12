
from telegram import  Update
from telegram.ext import Application , CommandHandler, JobQueue
from GiphyViewScrapper import get_giphy_views
from config import  TOKEN

# Replace with your Telegram Bot Token
BOT_TOKEN = TOKEN

# Update interval in seconds (adjust as needed)
UPDATE_INTERVAL = 86400  # 24 hours

# Variable to store previous day's view count
previous_views_dict = {}

async def send_daily_update(update, context):
    user_id = update.effective_user.id
    
    if user_id not in previous_views_dict:
        previous_views_dict[user_id] = 0
    try:
        url = update.message.text.split()[-1]
        current_views = get_giphy_views(url)
        current_int = int(current_views.split()[0].replace(",", ""))
        daily_views = current_int - previous_views_dict[user_id]
        previous_views_dict[user_id] = current_int

        message = f"Your Giphy project '{url}'.\n Has gained {daily_views} views today! and Total view : {current_views}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        await update.message.reply_text(f"Oops.\nFormat should be '/views <link>'")

async def start(update, context):
        username = update.message.from_user
        await update.message.reply_text(
            f"Hi! {username.first_name}.\nI'm the Giphy Views Tracker Bot.\nSend me a command like '/view [Gif Link]' to track your project's daily views.\nFor example : /view <link of the gif will be availabe in the share component or copy the url and paste>"
        )
        
async def help_command(update: Update, context) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text(
                "This is a Giphy Views Tracker Bot.\n"
                "You can use the following commands:\n"
                "/start - Start the bot and get instructions.\n"
                "/views - Track your Giphy project's daily views.\n"
                "/help - Get help and information about available commands."
        )


def main():
    
        proxy_url = "http://frwfguep:xowsusda97rnxowsusda97rn@38.154.227.167:5868"
        application = Application.builder().token(BOT_TOKEN).proxy().get_updates_proxy(proxy_url).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("views", send_daily_update))
        application.add_handler(CommandHandler("help", help_command))
        
        job=JobQueue()
        job.run_repeating(callback=send_daily_update, interval=UPDATE_INTERVAL, first=0)

        application.run_polling()
        
           

if __name__ == "__main__":
    main()