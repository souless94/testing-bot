import telebot
import creds
from telebot import types
from flask import Flask, request
import os
# helper functions

# def logToFile():
#     # code reused from labheshr 
#     # at https://stackoverflow.com/questions/33711475/python-logging-only-to-file
#     import logging
#     logging.basicConfig(filename='bot.log', level=logging.DEBUG,
#                     format=' %(asctime)s - %(levelname)s - %(message)s')
#     logging.info("logging file")


def extract_args(args):
    """a function that takes in a string and then split in spaces and remove the command word"""
    return args.split()[1:]

def is_positive_float(arg):
    try:
        isFloat = float(arg)
        return isFloat >= 0
    except ValueError:
        return False

#############################

# logging
# logToFile() # logging that only save to file

#######################################
#server
heroku_server = Flask(__name__)

######################################
# credentials
token = creds.token
bot = telebot.TeleBot(token = token)

################################

COMMANDS = {'bill':'bill [amount] [service charge] \n gets the bill amount after accounting for gst(7%) and service charge','help':'gets help on the commands','question':'question [name] \n creates a poll','result':'gets results of poll','reset_poll':'resets the poll'}
history = {}
# handlers

@bot.message_handler(commands = ['bill'])
def send_bill(message):
    gst = 0.07 # 7% gst
    ans = [0,0] # first input is amount 2nd input is service charge
    userInputs = extract_args(message.text)
    userInputs.extend([0,0])
    print(userInputs)
    ans[0] = userInputs[0]
    ans[1] = userInputs[1]
    response = list(map(is_positive_float,ans))
    if (False in response):
        bot.reply_to(message,"invalid input")
    else:
        amount = round(float(ans[0]),2)
        service_charge = round(float(ans[1]),2)
        finalamount = round(amount * (1+gst+service_charge),2)
        bot.reply_to(message,"amount is : ${} with a service charge of ${}".format(finalamount,service_charge*amount))

@bot.message_handler(commands = ['help'])
def command_help(message):
    help_msg = ""
    for command, desc in COMMANDS.items():
        help_msg += command + " : " + desc + "\n"
        help_msg += "-----------------\n"
    bot.reply_to(message,"Here are the commands: \n {}".format(help_msg))
 
@bot.message_handler(commands = ['question'])
def get_answer(message):
    # adapted code from https://www.mindk.com/blog/how-to-develop-a-chat-bot/
    rm = types.InlineKeyboardMarkup()
    UserInput = extract_args(message.text)
    UserInput.extend([""])
    name = "".join(UserInput)
    rm.add(types.InlineKeyboardButton("already here", callback_data="already here"))
    rm.add(types.InlineKeyboardButton("on the way", callback_data="on the way"))
    rm.add(types.InlineKeyboardButton("still at home", callback_data="still at home"))
    rm.add(types.InlineKeyboardButton("not coming", callback_data="not coming"))
    bot.send_message(message.chat.id, '{} where are you?'.format(name), reply_markup=rm)
    
    
@bot.callback_query_handler(func=lambda call: call.data in ["already here","on the way","still at home","not coming"])
def test_callback(query):
    ans = query.data
    name = query.from_user.first_name
    history[str(name)] =str(ans)
    bot.answer_callback_query(query.id , text = "eh i am {} and i am ".format(name) + str(ans))
    bot.edit_message_text(text= "eh i am {} and i am ".format(name) + str(ans),chat_id =query.message.chat.id ,message_id = query.message.message_id)

@bot.message_handler(commands = ['result'])
def display_result(message):
    reply_string = ""
    for name, response in history.items():
        reply_string += "{} \t {} \n".format(name,response)
    positive_answer = list(history.values())
    positive = list(filter( lambda x : x == "yes", positive_answer))
    reply_string += "------------------ \n"+"People replied : {} \n".format(len(history))
    reply_string += "People agreed : {} | People disagreed : {} \n".format(len(positive),len(history) - len(positive))
    bot.send_message(message.chat.id, reply_string)

@bot.message_handler(commands = ['reset_poll'])
def reset_poll(message):
    history.clear()
    bot.send_message(message.chat.id,"poll reseted")
    
################################
#server routes
@heroku_server.route("/"+token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!",200

@heroku_server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook("https://telebotfin.herokuapp.com/"+token)
    return "!",200

if __name__ == "__main__":
    heroku_server.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))

