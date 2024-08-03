git checkout main
git pull
docker build -t squirrel-bot:latest ../
docker stop squirrel-bot
docker rm squirrel-bot
docker run -d -v /opt/squirrel-bot/bot-data:/usr/src/bot/data --name squirrel-bot squirrel-bot:latest
