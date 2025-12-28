import config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import os
from random import randint
from logic import DB_Manager

bot = telebot.TeleBot(config.API_TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBNAME = os.path.join(BASE_DIR, 'videogames.db')

manager = DB_Manager(DBNAME)

def send_game_info(bot, message, row):
    info = f"""
🎮 Game title:        {row[1]}
🕹 Platform:         {row[2]}
📅 Release year:     {row[3]}
🏷 Genre:            {row[4]}
🏢 Publisher:        {row[5]}

⭐ Critic score:     {row[6]} ({row[7]} reviews)
👤 User score:       {row[8]}
👨‍💻 Developer:      {row[9]}
🔞 Rating:           {row[10]}
"""
    bot.send_message(message.chat.id, info)


def main_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('/random'))
    return markup



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        """🎮 Welcome to the Video Game Bot!

Here you can find hundreds of video games 🔥
👉 Press /random to get a random game
👉 Or type the name of a game and I will try to find it!
""",
        reply_markup=main_markup()
    )


@bot.message_handler(commands=['random'])
def random_game(message):
    game = manager.random_game()[0]
    send_game_info(bot, message, game)


@bot.message_handler(func=lambda message: True)
def find_game_by_name(message):
    game = manager.find_game_by_name(message.text.lower())
    if game:
        bot.send_message(message.chat.id, "🎯 I found this game!")
        send_game_info(bot, message, game[0])
    else:
        bot.send_message(message.chat.id, "❌ I don't know this game 😔")


bot.infinity_polling()
