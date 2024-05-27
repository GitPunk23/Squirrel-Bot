FROM python:3

# Upgrade pip and install python-dotenv
RUN python -m pip install --upgrade pip
RUN python -m pip install python-dotenv

# Install discord.py
RUN python -m pip install discord.py

# Set the working directory
WORKDIR /usr/src/bot

# Copy repo into container
COPY . .

# Create a directory for bot data
RUN mkdir /usr/src/bot/data

# Set the command to run your bot.py script
CMD [ "python3", "bot.py" ]
