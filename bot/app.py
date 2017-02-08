import os
import sys
import asyncio
import telepot
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from pydub import AudioSegment


class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    async def handle_file(self, msg):
        user_id = msg['from']['id']
        file_id = msg['document']['file_id']
        file_name = msg['document']['file_name']
        await bot.download_file(file_id, '/tmp/%s.opus' % file_name)
        audio = AudioSegment.from_file('/tmp/%s.opus' % file_name)
        res = audio.export('%s.mp3' % file_name, format='mp3')
        await bot.sendPhoto(user_id, res)

    async def on_chat_message(self, msg):
        await self.handle_file(msg)


ACCESS_TOKEN = os.getenv("TELEGRAM_API_KEY")


if not ACCESS_TOKEN:
    exit()

bot = telepot.aio.DelegatorBot(ACCESS_TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
loop.run_forever()
