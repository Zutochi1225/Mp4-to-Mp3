import os
import telebot
from moviepy.editor import VideoFileClip

# Get bot token from environment variables
bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Send video to convert to MP3.")

# /bi command handler
@bot.message_handler(commands=['bi'])
def echo_message(message):
    # User ထည့်သွင်းထားသော command message ကို ပြန်လည်ပြောပါ
    user_message = message.text.split('/bi ', 1)[1] if len(message.text.split('/bi ')) > 1 else ''
    if user_message:
        bot.send_message(message.chat.id, f'You said: {user_message}')
    else:
        # Custom message for empty input
        bot.send_message(message.chat.id, "This Bot is made by Myanmar. This Bot is free to use. No need join group/channel.")

# Video to MP3 conversion handler
@bot.message_handler(content_types=['video'])
def convert_mp4_to_mp3(message):
    file_info = bot.get_file(message.video.file_id)
    file = bot.download_file(file_info.file_path)

    with open("video.mp4", "wb") as f:
        f.write(file)

    video = VideoFileClip("video.mp4")
    video.audio.write_audiofile("audio.mp3")

    with open("audio.mp3", "rb") as audio:
        bot.send_audio(message.chat.id, audio)

    os.remove("video.mp4")
    os.remove("audio.mp3")

# Start polling
bot.polling()
