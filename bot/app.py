import os
import sys
import asyncio
import telepot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from pydub import AudioSegment


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        if msg['document']:
            user_id = msg['from']['id']
            file_id = msg['document']['file_id']
            file_name = msg['document']['file_name']
            bot.download_file(file_id, '/tmp/%s.opus' % file_name)
            audio = AudioSegment.from_file('/tmp/%s.opus' % file_name)
            res = audio.export('/tmp/%s.mp3' % file_name, format='mp3')
            bot.sendAudio(user_id, open('/tmp/%s.mp3' % file_name, 'rb'))


ACCESS_TOKEN = os.getenv("TELEGRAM_API_KEY")


if not ACCESS_TOKEN:
    exit()

bot = telepot.DelegatorBot(ACCESS_TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])

bot.message_loop(run_forever='Listening ...')
# loop = asyncio.get_event_loop()
# loop.create_task(bot.message_loop())
# loop.run_forever()
