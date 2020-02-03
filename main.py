import os
import time
import datetime
import threading
import subprocess
from pprint import pprint
import telepot
import speech_recognition
from redacted import API_KEY


def chat(msg):
    """on chat message"""
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'voice':
        pprint(msg)
        threading.Thread(target=listen, args=[msg]).start()


def listen(msg):
    """listen to voice recording"""
    preview = bot.sendMessage(msg['chat']['id'], "Downloaden...", reply_to_message_id=msg['message_id'])
    msg_identifier = telepot.message_identifier(preview)
    file_path_ogg = download(msg)
    bot.editMessageText(msg_identifier, "Transcoden...")
    file_path_wav = transcode(file_path_ogg)
    bot.editMessageText(msg_identifier, "Transcriben...")
    text = transcribe(file_path_wav)
    bot.editMessageText(msg_identifier, text)


def download(msg) -> str:
    """download OGG file"""
    file_name = '_'.join([msg['from'].get('first_name'),
                          msg['from'].get('last_name'),
                          datetime.datetime.now().strftime('%c').replace(' ', '').replace(':', '')])
    file_path = f"voice/{file_name}.ogg".lower()
    bot.download_file(msg['voice']['file_id'], file_path)
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
        return recognizer.recognize_google(audio, None, "nl_NL")
    except speech_recognition.UnknownValueError:
        return "???"
    except speech_recognition.RequestError as e:
        print(e)
        return "Er ging iets mis, sorry"


if __name__ == '__main__':
    # Ensure voice/ dir
    if not os.path.exists("voice/"):
        os.makedirs("voice/")

    bot = telepot.Bot(API_KEY)
    recognizer = speech_recognition.Recognizer()
    bot.message_loop({'chat': chat})
    print('Listening...')
    while 1:
        time.sleep(10)
