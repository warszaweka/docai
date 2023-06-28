import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import documentai_v1

TOKEN = ''
NAME = ''


def start(update: Update, context):
    update.message.reply_text('start')


def handle_document(update: Update, context):
    file_id = update.message.document.file_id
    file_path = f'downloads/{file_id}'
    context.bot.get_file(file_id).download(file_path)
    try:
        client = documentai_v1.DocumentProcessorServiceClient()

        with open(file_path, 'rb') as file:
            content = file.read()

        inline_document = documentai_v1.Document(content=content, mime_type=update.message.document.mime_type)

        request = documentai_v1.ProcessRequest(
            inline_document=inline_document,
            name=NAME,
        )

        response = client.process_document(request=request)

        update.message.reply_text(f'Extracted text:\n{response.document.text}')
    finally:
        os.remove(file_path)


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
