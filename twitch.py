import os
from twitchio.ext import commands
from logging import getLogger; logger = getLogger('AIStreamer')
from utils import Queue, Config

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.getenv("TWITCH_TOKEN"), prefix='!', initial_channels=["#" + Config.get_value("twitch_username")])
        self.message_queue = Queue(5)

    async def event_ready(self):
        logger.info(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.echo or message.author.name.lower() == self.nick.lower():
            return
    
        if message.content.startswith('!question'):
            message.content = message.content.replace('!question', '').strip()
            if message.content and len(message.content) < 100 and len(message.content) > 5:
                self.message_queue.enqueue(message)
