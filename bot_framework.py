from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from get_rail_info import get_availability_info, pnr_status


# Global Variables
TelegramAPI_token = "Your Telegram Token"

railways_api_url = "https://api.railwayapi.com/v2/"
pnr_url = "https://api.railwayapi.com/v2/live/train/<train number>/date/<dd-mm-yyyy>/apikey/<apikey>/"
Seat_availability_url = "https://api.railwayapi.com/v2/check-seat/train/<train number>/source/<stn code>/dest/<dest code>/date/<dd-mm-yyyy>/pref/<class code>/quota/<quota code>/apikey/<apikey>/"


# Creating Updater and Dispatcher objects
updater = Updater(TelegramAPI_token)
dispatcher = updater.dispatcher


# Testing Command Handler Function 
def hello_handler(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


# Defining "PNR Status" Handler Function 
def pnr_status_handler(bot, update,args):
	print("In pnr function")
	if (not args):
		bot.send_message(chat_id=update.message.chat_id, text="Please enter the PNR number")
		return -1
	elif(len(args) >= 2):
		bot.send_message(chat_id=update.message.chat_id, text="Please enter the single valid PNR number")
		return -1

	pnr = str(args[0])
	print(pnr)
	output_text = pnr_status(pnr)
	bot.send_message(chat_id=update.message.chat_id, text=output_text)


# Defining "Train Availability" Handler Function
def train_availability_handler(bot, update, args):
	train_no = str(args[0])
	src_stn = str(args[1])
	des_stn = str(args[2])
	date = str(args[3])
	class_code = str(args[4])
	quota = str(args[5])

	availability_info = get_availability_info(train_no,src_stn,des_stn,date,class_code,quota)
	bot.send_message(chat_id=update.message.chat_id, text=availability_info)


# Testing Message Handler Function
def message_handler(bot,update):
	net_args = update.message.text
	net_args = net_args[::-1]
	print("cool")
	bot.send_message(chat_id=update.message.chat_id, text=net_args)


# Handling Command Handler Errors
def unknown_command_handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


# Calling Handler Functions
dispatcher.add_handler(CommandHandler('hello', hello_handler))
dispatcher.add_handler(CommandHandler('pnr', pnr_status_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('trainAvailability', train_availability_handler, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
dispatcher.add_handler(MessageHandler(Filters.command, unknown_command_handler))

# Using Continuous Pooling
updater.start_polling()
updater.idle()
