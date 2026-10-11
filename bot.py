import os
import sqlite3
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
DB = "mining.db"


def setup_database():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user.id,),
    )
    conn.commit()
    conn.close()

    await update.message.reply_text(
        "Welcome to BAKO MAFIA MINING! ⛏️\n\n"
        "Commands:\n"
        "/mine - Mine virtual coins\n"
        "/balance - Check your balance"
    )


async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,),
    )
    conn.execute(
        "UPDATE users SET balance = balance + 10 WHERE user_id = ?",
        (user_id,),
    )
    conn.commit()
    balance = conn.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]
    conn.close()

    await update.message.reply_text(
        f"⛏️ You mined 10 virtual coins!\n"
        f"Your balance: {balance}"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,),
    )
    conn.commit()
    balance = conn.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]
    conn.close()

    await update.message.reply_text(
        f"💰 Your balance: {balance} virtual coins"
    )


def main():
    if not TOKEN:
        raise RuntimeError("Please configure the BOT_TOKEN environment variable.")

    setup_database()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mine", mine))
    app.add_handler(CommandHandler("balance", balance))

    print("BAKO MAFIA MINING bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
