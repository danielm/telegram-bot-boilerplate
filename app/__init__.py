from flask import Flask
import telegram

from app.credentials import TOKEN

app = Flask(__name__)

bot = telegram.Bot(token=TOKEN)

from app import routes