import telebot
import threading
from time import sleep
import re
import requests
import json
from datetime import datetime, timezone

# from telegram.ext import *

BOT_TOKEN = "5190674601:AAFUYzm8Pa2mMjeyYXnaRCQHdWUyGhEZN80"
BOT_INTERVAL = 3 #3
BOT_TIMEOUT = 10 #30

# bot = None #Keep the bot object as global variable if needed

def bot_polling():
    #global bot #Keep the bot object as global variable if needed
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions(bot) #If bot is used as a global variable, remove bot as an input param
            # bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
            bot.polling()
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop
        sleep(4)

def botactions(bot):
    #Set all your bot handlers inside this function
    #If bot is used as a global variable, remove bot as an input param
    
    @bot.message_handler(commands=["start"])
    def command_start(message):
        release_date_temp=""
        while True:
            string1=""
            sleep(2)
            res = requests.get('https://www.globenewswire.com/JSonFeed')
            list_data = json.loads(res.text)
            # print(list_data)
            # print('---------')
            if release_date_temp!=list_data[0]["ReleaseDateTime"]:
                
                print('release_date_temp='+release_date_temp)
                print('ReleaseDateTime='+list_data[0]["ReleaseDateTime"])
                string1 = "*Title*\n"+list_data[0]["Title"]+"\n" + \
                    "*ReleaseDate*\n"+list_data[0]["ReleaseDateTime"]+'\n'
                release_date_temp=list_data[0]["ReleaseDateTime"]
                utc_dt = datetime.now(timezone.utc)
                date_time = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                string1 += "*ReceiveDate*\n"+date_time
                bot.reply_to(message, string1, parse_mode='Markdown')
                   
                # bot.reply_to(message, "Hi there!")
            
    

polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


#Keep main program running while bot runs threaded
if __name__ == "__main__":
    while True:
        try:
            sleep(2) #120
            # print('main')
        except KeyboardInterrupt:
            break