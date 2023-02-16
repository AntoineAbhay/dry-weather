# dry-weather
A Discord bot that tells when the weather is the driest according to meteo france forecast


## Using docker
```
docker build --tag dry-bot .
docker run -d --restart always -e "DISCORD_TOKEN=XXX" -e "DISCORD_CHANNEL_ID=123" -e "CITY=Paris" dry-bot
```