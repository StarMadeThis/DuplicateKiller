from telegram.ext import Updater, MessageHandler, Filters
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Path to the "seen.txt" file
seen_file_path = os.path.join(os.path.dirname(__file__), 'seen.txt')

# Load existing unique file IDs from the file
if os.path.exists(seen_file_path):
    with open(seen_file_path, 'r') as f:
        file_ids_seen = set(f.read().splitlines())
else:
    file_ids_seen = set()

def save_seen_file_ids():
    with open(seen_file_path, 'w') as f:
        f.write('\n'.join(file_ids_seen))

def handle_new_file(update, context):
    if update.message.photo:
        file_unique_id = update.message.photo[-1].file_unique_id
    elif update.message.document:
        file_unique_id = update.message.document.file_unique_id
    else:
        return

    if file_unique_id in file_ids_seen:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    else:
        file_ids_seen.add(file_unique_id)
        save_seen_file_ids()

file_handler = MessageHandler(Filters.document | Filters.photo, handle_new_file)
dispatcher.add_handler(file_handler)

updater.start_polling()
updater.idle()
