from flask import request, make_response

import telegram

from app import app, bot
from functools import wraps

from app.credentials import TOKEN, URL, CUSTOM_USERNAME, CUSTOM_PASSWORD, bot_user_name

from app.mastermind import get_response

#
# A simple decorator to protect some public URLs
#
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # FIXME: you should probably implement a better authentication system for production.
        if auth and auth.username == CUSTOM_USERNAME and auth.password == CUSTOM_PASSWORD:
            return f(*args, **kwargs)
        
        return make_response('Could not verify login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

#
# Default URL (not really used)
#
@app.route('/')
@auth_required
def index():
    return "Running {}...".format(bot_user_name)

#
# Set Telegram webhook URL
#
@app.route('/setwebhook', methods=['GET', 'POST'])
@auth_required
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

#
# Main Telegram 'callback' URL
#
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message is None:
        return 'ok'
    if update.message.chat is None:
        return 'ok'

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text
    if text is not None:
        text = update.message.text.encode('utf-8').decode()
        print("got text message :", text)

        response = get_response(text)
        if response is not None:
            bot.sendMessage(chat_id=chat_id, text=response)
            # , reply_to_message_id=msg_id

    return 'ok'