import os
import telebot
import yt_dlp

# আপনার টোকেনটি এখানে বসানো আছে
TOKEN = '8664744610:AAGGXWkAEj0Wzv8XsYq1R-9DSnE_VSjAvmI'
bot = telebot.TeleBot(TOKEN)

# ফোল্ডার না থাকলে তৈরি করে নেবে
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! যেকোনো ভিডিওর লিংক দিন, আমি 4K বা সর্বোচ্চ রেজুলেশনে ডাউনলোড করে দিচ্ছি।")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, "ভিডিও প্রসেস ও ডাউনলোড করা হচ্ছে, দয়া করে একটু অপেক্ষা করুন...")

    ydl_opts = {
        'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            file_path = base + '.mp4'

        bot.reply_to(message, "ডাউনলোড সম্পন্ন! টেলিগ্রামে আপলোড করা হচ্ছে...")
        
        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        # ফাইল পাঠানোর পর সার্ভার থেকে ডিলিট করে দেওয়া
        os.remove(file_path)
        
    except Exception as e:
        bot.reply_to(message, f"দুঃখিত, কোনো সমস্যা হয়েছে: {str(e)}")

# বট রান করার জন্য
print("বট চালু হয়েছে...")
bot.infinity_polling()