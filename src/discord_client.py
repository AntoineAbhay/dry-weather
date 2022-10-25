import os
from datetime import time
import discord
from discord.ext import tasks
from meteo_france_client import MyMeteoFranceClient


DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
assert DISCORD_TOKEN
DISCORD_CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID"))
assert DISCORD_CHANNEL_ID
CITY = os.environ.get("CITY", "Paris")


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.send_driest_moment_task.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def send_driest_moment(self, channel):
        meteo_client = MyMeteoFranceClient()
        (short_message, complete_message) = meteo_client.get_dry_weather_messages(CITY)
        discord_message = await channel.send(short_message)
        thread = await discord_message.create_thread(
            name="Driest times", auto_archive_duration=24 * 60
        )
        await thread.send(complete_message)

    @tasks.loop(time=time(hour=6))  # task runs at 6am everyday
    async def send_driest_moment_task(self):
        print("Send driest moment started")
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        await self.send_driest_moment(channel)
        print("Send driest moment finished")

    @send_driest_moment_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user.id in message.raw_mentions:
            print("Received a message for me !")
            await self.send_driest_moment(message.channel)


client = MyClient(intents=discord.Intents.default())
client.run(DISCORD_TOKEN)
