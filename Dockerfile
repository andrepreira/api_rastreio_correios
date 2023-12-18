# Use a Python 3.10 runtime as a parent image
FROM python:3.10

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# Set the working directory to /app
WORKDIR /app
RUN mkdir __logger

# Copy the Pipfile and Pipfile.lock files to the container
COPY Pipfile Pipfile.lock /app/

# install pyaudio libs
RUN apt-get apt-get install python3-pyaudio
RUN apt-get install -y portaudio19-dev python-all-dev python3-all-dev

# Install pipenv and dependencies from Pipfile.lock
RUN pip install --upgrade pip
RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copy the application code to the container
COPY src/. /app/

# Expose port 8080 for the application
EXPOSE 8080

# Start the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
