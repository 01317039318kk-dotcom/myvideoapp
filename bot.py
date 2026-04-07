import telebot
import yt_dlp
import os

# আপনার টেলিগ্রাম বোট টোকেন
BOT_TOKEN = "8713649037:AAFE9N4EgXriROEKPT4US7EL297c4qb405I"
bot = telebot.TeleBot(BOT_TOKEN)

# ডাউনলোড করা ফাইল রাখার ফোল্ডার
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "স্বাগতম! আমাকে একটি YouTube ভিডিও লিঙ্ক পাঠান।")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = bot.reply_to(message, "ভিডিওটি প্রসেসিং হচ্ছে, দয়া করে অপেক্ষা করুন...")
        
        # ডাউনলোডের সেটিংস
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            # বোটের মাধ্যমে ভিডিও পাঠানো
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=info.get('title'))
            
            # কাজ শেষ হলে ফাইল মুছে ফেলা
            os.remove(filename)
            bot.delete_message(message.chat.id, status_msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"ভুল হয়েছে: {str(e)}", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "অনুগ্রহ করে সঠিক ইউটিউব লিঙ্ক পাঠান।")

print("বোটটি সচল আছে...")
bot.infinity_polling()

