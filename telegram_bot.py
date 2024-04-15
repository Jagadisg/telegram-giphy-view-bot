from telegram import  Update
from telegram.ext import Application , CommandHandler, ContextTypes
from GiphyViewScrapper import get_giphy_views
from config import  TOKEN
from datetime import time


# Replace with your Telegram Bot Token
BOT_TOKEN = TOKEN

# Variable to store previous day's view count
previous_views_dict = {}


async def send_daily_update(update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in previous_views_dict:
        previous_views_dict[user_id] = {
            "views" : 0,
            "url" : update.message.text.split()[-1],
            "chat_id" : update.effective_chat.id
        }
    try:
        url = update.message.text.split()[-1]
        current_views = get_giphy_views(url)
        current_int = int(current_views.split()[0].replace(",", ""))
        daily_views = current_int - previous_views_dict[user_id]["views"]
        previous_views_dict[user_id]["views"] = current_int
        try:
            context.job_queue.run_daily(callback=lambda context: daily_update(update, context),time=time(hour=1,minute=0),chat_id=update.effective_chat.id,user_id=update.effective_user.id)
        except Exception as e:
            print(e)
        message = f"Your Giphy project `{url}`.\n Has gained {daily_views} views today! and Total view : {current_views}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        await update.message.reply_text(f"Oops.\nFormat should be '/views <link>'")


async def start(update, context:ContextTypes.DEFAULT_TYPE):
        username = update.message.from_user
        await update.message.reply_text(
            f"Hi! {username.first_name}.\nI'm the Giphy Views Tracker Bot.\nSend me a command like '/view [Gif Link]' to track your project's daily views.\nFor example : /view <link of the gif will be availabe in the share component or copy the url and paste>"
        )

        
async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text(
                "This is a Giphy Views Tracker Bot.\n"
                "You can use the following commands:\n"
                "/start - Start the bot and get instructions.\n"
                "/views - Track your Giphy project's daily views.\n"
                "/help - Get help and information about available commands."
                "/change - Change the project gif link you want to track views"
        )

        
async def daily_update(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
            print("daily")
            job=context.job
            current_views = get_giphy_views(previous_views_dict[job.user_id]["url"])
            current_int = int(current_views.split()[0].replace(",", ""))
            daily_views = current_int - previous_views_dict[job.user_id]["views"]
            previous_views_dict[job.user_id]["views"] = current_int

            message = f"Your Giphy project `{previous_views_dict[job.user_id]['url']}`.\n Has gained {daily_views} views today! and Total view : {current_views}"
            await context.bot.send_message(chat_id=previous_views_dict[job.user_id]["chat_id"], text=message)


async def change_gif(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        if user_id in previous_views_dict or user_id not in previous_views_dict:
            previous_views_dict[user_id] = {
                "views" : 0,
                "url" : update.message.text.split()[-1],
                "chat_id" : update.effective_chat.id
            }
        await update.message.reply_text(f"Your Project Gif Changed")

            
def main():    
        proxy_url = "http://frwfguep:xowsusda97rn@38.154.227.167:5868"
        application = Application.builder().token(BOT_TOKEN).proxy(proxy_url).get_updates_proxy(proxy_url).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("views", send_daily_update))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("change",change_gif))

        application.run_polling()
        
          
           
if __name__ == "__main__":
    main()