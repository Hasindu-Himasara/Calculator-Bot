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


CALCULATE_TEXT = "Altex's Calculator Menu"

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
            InlineKeyboardButton("TAN", callback_data="tan"),
            InlineKeyboardButton("%", callback_data="perc")
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
                    await update.answer("Empty input.")
                    return
                else:
                    try:
                        text = float(eval(message_text))
                    except:
                        await update.answer("Syntax Error.")
                        return
            elif data == "sqrt":
                try:
                    text = math.sqrt(Decimal(message_text))
                except:
                    await update.answer("Entered value is not a number.")
                    return
            elif data == "sin":
                try:
                    cal = math.sin(math.radians(Decimal(message_text)))
                    text = '{:.4f}'.format(cal)
                except:
                    await update.answer("Entered value is not a number.")
                    return
            elif data == "cos":
                try:
                    cal = math.cos(math.radians(Decimal(message_text)))
                    text = '{:.4f}'.format(cal)
                except:
                    await update.answer("Entered value is not a number.")
                    return
            elif data == "tan":
                try:
                    cal = math.tan(math.radians(Decimal(message_text)))
                    text = '{:.4f}'.format(cal)
                except:
                    await update.answer("Entered value is not a number.")
                    return
            elif data == "perc":
                try:
                    text = Decimal(message_text) / 100
                except:
                    await update.answer("Entered value is not a number.")
                    return                                 
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


Bot.run()
