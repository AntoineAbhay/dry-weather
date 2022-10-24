import os
from datetime import time
import discord
from discord.ext import tasks
from meteo_france_client import MyMeteoFranceClient
from aggregate_data import aggregate_data
from message import get_complete_message, get_driest_moments_message

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
assert DISCORD_TOKEN
DISCORD_CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID"))
assert DISCORD_CHANNEL_ID
CITY = os.environ.get("CITY", "Paris")
NB_DAYS_FROM_NOW = [2, 7]
HUMIDITY_THRESHOLD = 70


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.send_driest_moment.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    @tasks.loop(time=time(hour=6))  # task runs at 6am everyday
    async def send_driest_moment(self):
        print("Send driest moment started")
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        meteo_client = MyMeteoFranceClient()
        next_days_data = meteo_client.get_next_days_data(CITY)
        aggregated_data = aggregate_data(next_days_data)
        discord_message = await channel.send(
            get_driest_moments_message(aggregated_data, NB_DAYS_FROM_NOW)
        )
        thread = await discord_message.create_thread(name="Driest times")
        await thread.send(get_complete_message(aggregated_data, HUMIDITY_THRESHOLD))
        print("Send driest moment finished")

    @send_driest_moment.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(DISCORD_TOKEN)
