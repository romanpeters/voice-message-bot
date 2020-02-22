import os
import time
import logging
import datetime
import threading
import subprocess
from pprint import pprint
import speech_recognition
import language
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from redacted import BOT_TOKEN
from pprint import pformat

# Set transcription language
L = language.Dutch


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" \n caused error "{context.error}"')


def listen(update, context):
    """listen to voice recording"""
    bot = context.bot
    reply = update.message.reply_text(L.DOWNLOADING)

    file_path_ogg = download(update)
    bot.edit_message_text(chat_id=update.message.chat_id, message_id=reply.message_id, text=L.TRANSCODING)
    file_path_wav = transcode(file_path_ogg)
    bot.edit_message_text(chat_id=update.message.chat_id, message_id=reply.message_id, text=L.TRANSCRIBING)
    text = transcribe(file_path_wav)
    bot.edit_message_text(chat_id=update.message.chat_id, message_id=reply.message_id, text=text)


def download(update) -> str:
    """download OGG file"""
    user = update.message.from_user
    file_name = '_'.join([user.first_name,
                          user.last_name if user.last_name else "",
                          datetime.datetime.now().strftime('%c').replace(' ', '').replace(':', '')])
    file_path = f"voice/{file_name}.ogg".lower()
    voice_file = update.message.voice.get_file()
    voice_file.download(file_path)
    return file_path


def transcode(ogg_file: str) -> str:
    """transcode OGG file to WAV file"""
    new_path = ogg_file.replace(".ogg", ".wav")
    subprocess.run(['ffmpeg', '-i', ogg_file, new_path])
    os.remove(ogg_file)
    return new_path


def transcribe(wav_file: str) -> str:
    """transcribe WAV file"""
    audio_file = speech_recognition. AudioFile(wav_file)
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, None, L.LANGUAGE)
    except speech_recognition.UnknownValueError:
        return L.UNKNOWN_VALUE
    except speech_recognition.RequestError as e:
        print(e)
        return L.REQUEST_ERROR



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.voice, listen))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print("Listening...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # Ensure voice/ dir
    if not os.path.exists("voice/"):
        os.makedirs("voice/")

    recognizer = speech_recognition.Recognizer()

    main()

