FROM python:3.8-slim

# Install wget, unzip, and Chrome browser
RUN apt-get update \
    && apt-get install -y wget unzip gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Download and install chromedriver
RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Set up and install Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy bot and scraper files into the container
COPY telegram_bot.py GiphyViewScrapper.py config.py /app/

# Start the bot
CMD ["python", "telegram_bot.py"]
