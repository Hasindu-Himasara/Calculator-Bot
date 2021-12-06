import os
import math
from decimal import Decimal
from pyrogram import Client, filters
from pyrogram.types import *


Bot = Client(
    "Calculator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


START_TEXT = """**Hola {} 👋**

I am a simple calculator telegram bot, send /calc to use me!"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("GitHub", url="https://github.com/ImJanindu")
        ]
    ]
)

CALCULATE_TEXT = "Smart telegram calculator :/"

CALCULATE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⌫", callback_data="DEL"),
            InlineKeyboardButton("AC", callback_data="AC"),
            InlineKeyboardButton("√", callback_data="sqrt"),
            InlineKeyboardButton("(", callback_data="("),
            InlineKeyboardButton(")", callback_data=")")
        ],
        [
            InlineKeyboardButton("SIN", callback_data="sin"),
            InlineKeyboardButton("COS", callback_data="cos"),
            InlineKeyboardButton("TAN", callback_data="tan")
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
            InlineKeyboardButton("÷", callback_data="/")
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
            InlineKeyboardButton("×", callback_data="*")
        ],
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
            InlineKeyboardButton("-", callback_data="-"),
        ],
        [
            InlineKeyboardButton(".", callback_data="."),
            InlineKeyboardButton("0", callback_data="0"),
            InlineKeyboardButton("=", callback_data="="),
            InlineKeyboardButton("+", callback_data="+"),
        ]
    ]
)


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@Bot.on_message(filters.private & filters.command(["calc", "calculate", "calculator"]))
async def calculate(bot, update):
    await update.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_callback_query()
async def cb_data(bot, update):
        data = update.data
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            message_text = '' if CALCULATE_TEXT in message_text else message_text
            if data == "=":
                if message_text == "":
                    text = "Empty input."
                else:
                    try:
                        text = float(eval(message_text))
                    except:
                        text = "Syntax Error."
            elif data == "sqrt":
                try:
                    if "." in message_text:
                        omk = Decimal(message_text)
                        text = math.sqrt(omk)
                    else:
                        text = math.sqrt(int(message_text))
                except:
                    text = "Entered value is not a number."
            elif data == "sin":
                try:
                    cal = math.sin(math.radians(int(message_text)))
                    text = '{:.4f}'.format(cal)
                except:
                    text = "Entered value is not a number."
            elif data == "cos":
                try:
                    cal = math.cos(math.radians(int(message_text)))
                    text = '{:.4f}'.format(cal)
                except:
                    text = "Entered value is not a number."
            elif data == "tan":
                try:
                    cal = math.tan(math.radians(int(message_text)))
                    text = '{:.4f}'.format(cal)
                except:
                    text = "Entered value is not a number."
                
            elif data == "DEL":
                text = message_text[:-1]
            elif data == "AC":
                text = ""
            else:
                text = message_text + data
            await update.message.edit_text(
                text=f"{text}\n\n{CALCULATE_TEXT}",
                disable_web_page_preview=True,
                reply_markup=CALCULATE_BUTTONS
            )
        except Exception as e:
            print(str(e))


@Bot.on_inline_query()
async def inline(bot, update):
    if len(update.data) == 0:
        try:
            answers = [
                InlineQueryResultArticle(
                    title="Calculator",
                    description=f"New calculator",
                    input_message_content=InputTextMessageContent(
                        text=CALCULATE_TEXT,
                        disable_web_page_preview=True
                    ),
                    reply_markup=CALCULATE_BUTTONS
                )
            ]
        except Exception as e:
            print(str(e))
    else:
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            data = message_text.replace("×", "*").replace("÷", "/")
            text = float(eval(data))
            answers = [
                InlineQueryResultArticle(
                    title="Answer",
                    description=f"Results of your input",
                    input_message_content=InputTextMessageContent(
                        text=f"{data} = {text}",
                        disable_web_page_preview=True
                    )
                )
            ]
        except:
            pass
    await update.answer(answers)


Bot.run()
