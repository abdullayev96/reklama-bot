from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database

db = Database("database.db")

CHANNEL_ID = -1001261519461

def check(update, context):
    user = update.message.from_user
    db_user = db.get_user_chat_by_id(user.id)
    if not db_user:
        db.create_user(user.id)
        buttons = [
            [KeyboardButton(text="E'lon berish")]
        ]
        update.message.reply_text(
            text=f"Salom O'shlik kuyov 😍😍😍😍☺️☺️☺️😋😋😋🙃🙃🙃🥰🥰🥰🙂🙂🙂😉😉 {user.first_name}!\n"
                 f"Xush kelibsiz botimizga!",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        )
    elif not db_user["heading"]:
        update.message.reply_text(
            text="Reklama sarlavhasini kiriting",
            reply_markup=ReplyKeyboardRemove()
        )

    elif not db_user["main_heading"]:
        update.message.reply_text(
            text="Reklama sarlavhasini kiriting",
            reply_markup=ReplyKeyboardRemove()
        )

    elif not db_user["text"]:
        update.message.reply_text(
            text="Reklama matnini kiriting",
            reply_markup=ReplyKeyboardRemove()
        )
    elif not db_user["contact"]:
        update.message.reply_text(
            text="Telefon raqamingizni kiriting",
            reply_markup=ReplyKeyboardRemove()
        )
    elif not db_user["image"]:
        update.message.reply_text(
            text="Reklama rasmini yuboring",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        update.message.reply_text(
            text="Xabaringiz muvaffaqiyatli qabul qilindi. "
                 "Moderatorlarimiz xabaringiz tez orada tekshirishadi",
            reply_markup=ReplyKeyboardRemove()
        )
        context.bot.send_photo(
            photo=open(db_user["image"], "rb"),
            caption=f"<b>{db_user['main_heading']}</b>\n"
                    f"{db_user['text']}\n"
                    f"{db_user['contact']}\n",
            parse_mode="HTML",
            chat_id=697775505,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Tasdiqlash", callback_data=f"ok_{update.message.chat_id}")],
                [InlineKeyboardButton(text="Bekor qilish", callback_data=f"wrong_{update.message.chat_id}")]
            ])
        )

def inline_handler(update, context):
    query = update.callback_query
    data_sp = str(query.data).split("_")
    db_user = db.get_user_chat_by_id(int(data_sp[1]))
    if data_sp[0] == "ok":
        context.bot.send_message(
            chat_id=int(data_sp[1]),
            text="Tabriklaymiz O'shlik kuyov! E'loningiz tasdiqlandi!"
        )
        context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=open(db_user["image"], "rb"),
            caption=f"<b>{db_user['main_heading']}</b>\n"
                    f"{db_user['text']}\n"
                    f"{db_user['contact']}\n",
            parse_mode="HTML",
        )
    elif data_sp[0] == "ng":
        context.bot.send_message(
            chat_id=int(data_sp[1]),
            text="Tabriklaymiz O'shlik kuyov! E'loningiz tasdiqlanmadi! Battar bo'ling"
        )


def start(update, context):
    check(update, context)

def message_handler(update, context):
    message = update.message.text
    user = update.message.from_user
    db_user = db.get_user_chat_by_id(user.id)

    if not db_user["heading"]:
        db.update_user_data(user.id, "heading", message)
        check(update, context)
    elif not db_user["main_heading"]:
        db.update_user_data(user.id, "main_heading", message)
        check(update, context)
    elif not db_user["text"]:
        db.update_user_data(user.id, "text", message)
        check(update, context)
    elif not db_user["contact"]:
        db.update_user_data(user.id, "contact", message)
        check(update, context)
    else:
        check(update, context)


def photo_handler(update, context):
    user = update.message.from_user
    file = context.bot.get_file(update.message.photo[-1])
    file.download(f"demo_{update.message.chat_id}.jpg")
    db.update_user_data(user.id, "image", f"demo_{update.message.chat_id}.jpg")
    check(update, context)

def contact_handler(update, context):
    pass

def main():
    updater = Updater("1776334506:AAEg2YEfu28F4dWJ2WF9sNyXNBGe7tgi3Ps")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()