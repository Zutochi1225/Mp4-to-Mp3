import telebot
import moviepy.editor as mp
import os

# Telegram Bot Token
bot_token = os.getenv("BOT_TOKEN")  # Heroku မှာ BOT_TOKEN ကို Config Vars မှာ ထည့်ပါ
bot = telebot.TeleBot(bot_token)

# MP4 to MP3 ပြောင်းတဲ့ function
@bot.message_handler(content_types=['video'])
def convert_mp4_to_mp3(message):
    try:
        # Video ဖိုင် download
        file_info = bot.get_file(message.video.file_id)
        file = bot.download_file(file_info.file_path)
        
        # Video ဖိုင် သိမ်းထားရန်
        video_path = 'video.mp4'
        with open(video_path, 'wb') as f:
            f.write(file)

        # MP3 ဖိုင်သို့ ပြောင်းခြင်း
        video = mp.VideoFileClip(video_path)
        audio_path = 'audio.mp3'
        video.audio.write_audiofile(audio_path)
        
        # MP3 ဖိုင်ကို ပြန်ပေးပို့ခြင်း
        with open(audio_path, "rb") as audio:
            bot.send_audio(message.chat.id, audio)

        # ဖိုင်များကိုဖျက်ပစ်ခြင်း
        os.remove(video_path)
        os.remove(audio_path)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Conversion error occurred!")
        print(e)

# Bot ကို run ထားရန်
bot.polling()