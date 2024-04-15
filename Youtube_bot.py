import telebot
from pytube import YouTube
import os

TOKEN = '6813919333:AAH52gZi61Vk2Wq4_90-vVX7qNbKx3sRZqo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! قم بإرسال رابط الفيديو أو الصوت الذي ترغب في تنزيله.")

@bot.message_handler(func=lambda message: True)
def download_media(message):
    try:
        url = message.text
        yt = YouTube(url)
        bot.reply_to(message, "تم العثور على المحتوى! هل ترغب في تنزيل الفيديو أم الصوت فقط؟ (فيديو/صوت)")
        bot.register_next_step_handler(message, choose_format, yt)
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء معالجة الطلب: {str(e)}")

def choose_format(message, yt):
    try:
        user_response = message.text.lower()
        if user_response == 'فيديو':
            stream = yt.streams.get_highest_resolution()
            filename = stream.download()
            bot.send_video(message.chat.id, open(filename, 'rb'))
            os.remove(filename)
            bot.reply_to(message, "تم تنزيل الفيديو وإرساله لك.")
        elif user_response == 'صوت':
            stream = yt.streams.filter(only_audio=True).first()
            filename = stream.download()
            bot.send_audio(message.chat.id, open(filename, 'rb'))
            os.remove(filename)
            bot.reply_to(message, "تم تنزيل الصوت وإرساله لك.")
        else:
            bot.reply_to(message, "يرجى الرد ب 'فيديو' أو 'صوت'.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء معالجة الطلب: {str(e)}")

bot.polling()
