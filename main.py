import os, time, threading, logging, multiprocessing, uuid
from logger import create_logger; logger = create_logger('AIStreamer')
from flaskServer import server
from twitch import Bot
from dotenv import load_dotenv; load_dotenv()
from llmEngine import gen_gpt
from ttsEngine import gen_elevenlabs
import wav2lipEngine

if __name__ == "__main__":

    twitch_bot = Bot()
    twitch_bot_thread = threading.Thread(target=twitch_bot.run)
    twitch_bot_thread.daemon = True
    twitch_bot_thread.start()

    # flask_server_process = multiprocessing.Process(target=server.runServer)
    # flask_server_process.daemon = True
    # flask_server_process.start()

    while True:
        message = twitch_bot.message_queue.dequeue()
        if not message:
            time.sleep(1)
            continue
        logger.info(f"Message received: {message}")
        logger.info(f"Generating answer...")
        answer = gen_gpt(message)
        logger.info(f"Answer generated: {answer}")
        logger.info(f"Generating audio...")
        audio = gen_elevenlabs(answer)
        logger.info(f"Audio generated")
        logger.info(f"Generating video...")
        videoId = str(uuid.uuid4())[:8]
        wav2lipEngine.performInference(audio, videoId)
        with open(f"flaskServer/static/queue/{videoId}.txt", "w") as writer:
            writer.write(message)
        logger.info(f"Video generated")





