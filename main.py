import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext

# ==============================
# ⚠️ Replace with your NEW Bot Token
# ==============================
BOT_TOKEN = "8568040647:AAHrjk2CnFeKJ0gYFZQp4mDCKd02nyyOii0"
ADMIN_ID = 7301067810   # replace with your Telegram ID

LOG_FILE = "logs.txt"

# ==============================
# Replit Keep Alive Server
# ==============================
app = Flask("")

@app.route("/")
def home():
    return "Keyword Bot Running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==============================
# Search Function
# ==============================
def search_keywords(keywords):
    if not os.path.exists(LOG_FILE):
        return "⚠️ logs.txt not found."

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return "⚠️ Cannot read logs.txt"

    results = []

    for line in lines:
        for k in keywords:
            if k.lower() in line.lower():
                results.append(line.strip())
                break

    if not results:
        return "❌ No results found."

    return "🔍 *Search Results:*\n\n" + "\n".join(results[:60])  # limit

# ==============================
# Commands
# ==============================
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 Keyword Search Bot is online!\n\n"
        "Use:\n"
        "`/search <keyword>`\n"
        "`/search garena roblox`\n"
        "You can search multiple keywords.",
        parse_mode="Markdown"
    )

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📚 *Commands*\n"
        "/search <keyword> – Search inside logs.txt\n"
        "/stats – Show file lines\n"
        "/setfile <file> – Admin only\n"
        "/addlog <text> – Admin only\n",
        parse_mode="Markdown"
    )

def stats(update: Update, context: CallbackContext):
    if not os.path.exists(LOG_FILE):
        update.message.reply_text("⚠️ logs.txt missing.")
        return

    lines = sum(1 for _ in open(LOG_FILE, "r", encoding="utf-8"))
    update.message.reply_text(f"📊 File: {LOG_FILE}\nLines: {lines}")

def setfile(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ You’re not admin.")
        return

    global LOG_FILE
    if not context.args:
        update.message.reply_text("Usage: /setfile filename.txt")
        return

    LOG_FILE = context.args[0]
    update.message.reply_text(f"✅ File changed to {LOG_FILE}")

def addlog(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ You’re not admin.")
        return

    if not context.args:
        update.message.reply_text("Usage: /addlog text here")
        return

    entry = " ".join(context.args)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

    update.message.reply_text("✔️ Log added.")

# ==============================
# /search command
# ==============================
def search_cmd(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage:\n`/search <keyword>`", parse_mode="Markdown")
        return

    keywords = context.args
    result = search_keywords(keywords)
    update.message.reply_text(result, parse_mode="Markdown")

# ==============================
# Start Bot
# ==============================
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("setfile", setfile))
    dp.add_handler(CommandHandler("addlog", addlog))
    dp.add_handler(CommandHandler("search", search_cmd))

    updater.start_polling()
    updater.idle()

keep_alive()
main()