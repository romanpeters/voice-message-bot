## voice-message-bot

Add this bot to your Telegram chats to automatically transcribe any voice messages that get sent.

### Quick setup
```
$ git clone https://github.com/romanpeters/voice-message-bot.git
$ cd voice-message-bot
$ git submodule update --init
$ docker build . --tag build voice-message-bot:latest
$ docker-compose up
```
### Advanced setup
Optional additional setup steps:
- Uncomment the lines in `docker-compose.yml` and edit the volumes path.  
- Set your preferred language in `main.py` by changing the `L`-variable to a language from `language.py`.
- Add your Google API key to `main.py`.