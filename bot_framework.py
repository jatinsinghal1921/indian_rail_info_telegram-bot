from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from get_rail_info import RailInfoDayCount, RailInfoCreditCount

# Global Variables
TelegramAPI_token = "Your Telegram Token"

# Creating Updater and Dispatcher objects
updater = Updater(TelegramAPI_token)
dispatcher = updater.dispatcher


# Testing Command Handler Function 
def hello_handler(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


# Defining "PNR Status" Handler Function 
def pnr_status_handler(bot, update, args):
    print("In pnr function")
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text="Please enter the PNR number")
        return -1
    elif len(args) >= 2:
        bot.send_message(chat_id=update.message.chat_id, text="Please enter the single valid PNR number")
        return -1

    pnr = str(args[0])
    print(pnr)
    obj = RailInfoCreditCount()
    output_text = obj.pnr_status(pnr)
    bot.send_message(chat_id=update.message.chat_id, text=output_text)


# Defining "Seat Availability" Handler Function
def seat_availability_handler(bot, update, args):
    print("In Seat Availability function")
    if len(args) < 6:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter all the entries required for seat avalability")
        return -1
    elif len(args) > 6:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter valid entries required for seat avalability")
        return -1
    train_no = str(args[0])
    src_stn = str(args[1])
    des_stn = str(args[2])
    date = str(args[3])
    class_code = str(args[4])
    quota = str(args[5])
    print(train_no, src_stn, des_stn, date, class_code, quota)

    obj = RailInfoCreditCount()
    availability_info = obj.seat_availability_info(train_no, src_stn, des_stn, date, class_code, quota)
    bot.send_message(chat_id=update.message.chat_id, text=availability_info)


# Defining "Train Availability" Handler Function
def train_availability_handler(bot, update, args):
    print("In Train Availability function")
    if len(args) < 3:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter all the entries required for train avalability")
        return -1
    elif len(args) > 3:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter valid entries required for train avalability")
        return -1
    src_stn = str(args[0])
    des_stn = str(args[1])
    date = str(args[2])
    print(src_stn, des_stn, date)

    obj = RailInfoCreditCount()
    availability_info = obj.train_availability_info(src_stn, des_stn, date)
    for each_train in availability_info:
        bot.send_message(chat_id=update.message.chat_id, text=each_train)
    del obj


def train_fare_handler(bot, update, args):
    print("In Train Fare function")
    if len(args) < 4:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter all the entries required to get the Train Fare")
        return -1
    elif len(args) > 4:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter valid entries required to get the Train Fare")
        return -1
    train_no = str(args[0])
    src_stn = str(args[1])
    des_stn = str(args[2])
    quota = str(args[3])
    print(train_no, src_stn, des_stn, quota)

    obj = RailInfoDayCount()
    fare_info = obj.train_fare(train_no, src_stn, des_stn, quota)
    bot.send_message(chat_id=update.message.chat_id, text=fare_info)


def track_train_handler(bot, update, args):
    print("In Train Tracking function")
    if len(args) < 2:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter all the entries required to track the train")
        return -1
    elif len(args) > 2:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter valid entries required to track the train")
        return -1
    train_no = str(args[0])
    date = str(args[1])
    print(train_no, date)

    obj = RailInfoCreditCount()
    track_info = obj.track_train(train_no, date)
    bot.send_message(chat_id=update.message.chat_id, text=track_info)


def train_details_handler(bot, update, args):
    print("In Train Details function")
    if len(args) < 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Please enter either the train name or train number.")
        return -1
    elif len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="There are too many entries. Please enter either Train no. or Train name.")
        return -1
    train_no = str(args[0])
    print(train_no)

    obj = RailInfoCreditCount()
    train_info = obj.train_details(train_no)
    bot.send_message(chat_id=update.message.chat_id, text=train_info)


# Testing Message Handler Function
def message_handler(bot, update):
    net_args = update.message.text
    net_args = net_args[::-1]
    print("In message_handler function")
    bot.send_message(chat_id=update.message.chat_id, text=net_args)


# Handling Command Handler Errors
def unknown_command_handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


# Calling Handler Functions
dispatcher.add_handler(CommandHandler('hello', hello_handler))
dispatcher.add_handler(CommandHandler('pnr', pnr_status_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('seatAvailability', seat_availability_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('trainAvailability', train_availability_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('train_fare', train_fare_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('track_train', track_train_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('train_details', train_details_handler, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
dispatcher.add_handler(MessageHandler(Filters.command, unknown_command_handler))

# Using Continuous Pooling
updater.start_polling()
updater.idle()
