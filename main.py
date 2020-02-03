import time
import datetime
import subprocess
from pprint import pprint
import locale
import pytz
import telepot
import speech_recognition
from redacted import API_KEY

utc = pytz.timezone('CET')

try:
    locale.setlocale(locale.LC_TIME, "nl_NL.utf8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "nl_NL")


def chat(msg):
    """on chat message"""
    time.sleep(0.1)  # only necessary if reply from bot appears before command
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'voice':
        pprint(msg)
        print(msg['chat']['id'], msg['voice']['file_id'])
        listen(msg)


def listen(msg):
    preview = bot.sendMessage(msg['chat']['id'], "Downloading...")
    msg_identifier = telepot.message_identifier(preview)
    file_path_ogg = download(msg)
    bot.editMessageText(msg_identifier, "Transcoding...")
    file_path_wav = transcode(file_path_ogg)
    bot.editMessageText(msg_identifier, "Transcribing...")
    text = transcribe(file_path_wav)
    bot.editMessageText(msg_identifier, text)


def download(msg) -> str:
    file_name = '_'.join([msg['from'].get('first_name'),
                          msg['from'].get('last_name'),
                          datetime.datetime.now().strftime('%c').replace(' ', '').replace(':', '')])
    file_path = f"voice/{file_name}.ogg".lower()
    bot.download_file(msg['voice']['file_id'], file_path)
    return file_path


def transcode(ogg_file: str) -> str:
    new_path = ogg_file.replace(".ogg", ".wav")
    subprocess.run(['ffmpeg', '-i', ogg_file, new_path])
    return new_path


def transcribe(wav_file: str) -> str:
    audio_file = speech_recognition. AudioFile(wav_file)
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, None, "nl_NL")
    except speech_recognition.UnknownValueError:
        return "???"
    except speech_recognition.RequestError as e:
        print(e)
        return "Er ging iets mis, sorry"


if __name__ == '__main__':
    print('Listening...')
    bot = telepot.Bot(API_KEY)
    recognizer = speech_recognition.Recognizer()
    bot.message_loop({'chat': chat})
    while 1:
        time.sleep(10)
