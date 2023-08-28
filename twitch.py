import os
from twitchio.ext import commands
from logging import getLogger; logger = getLogger('AIStreamer')

class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.messages = []

    def enqueue(self, message):
        if len(self.messages) < self.capacity:
            self.messages.append(message)
    
    def dequeue(self):
        if len(self.messages) > 0:
            return self.messages.pop(0)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.getenv("TWITCH_TOKEN"), prefix='!', initial_channels=["#" + os.getenv("STREAMER_PSEUDO")])
        self.message_queue = Queue(5)

    async def event_ready(self):
        logger.info(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.echo or message.author.name.lower() == self.nick.lower():
            return
    
        # use message.raw_data maybe for channel point later
        if message.content.startswith('!question'):
            onlyContent = message.content.replace('!question', '').strip()
            if onlyContent and len(onlyContent) < 100 and len(onlyContent) > 5:
                self.message_queue.enqueue(onlyContent)

# bot = Bot()
# bot.run()