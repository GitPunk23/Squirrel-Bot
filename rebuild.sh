docker build -t SquirrelBot:latest .
docker stop SquirrelBot
docker rm SquirrelBot
docker run -d -v /home/squirrelbot/bot-data:/usr/src/bot/data --name SquirrelBot squirrelbot:latest