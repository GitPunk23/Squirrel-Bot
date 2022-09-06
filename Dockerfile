FROM python:3
FROM gorialis/discord.py

RUN python -m pip install python-dotenv
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

CMD [ "python3", "bot.py"]
