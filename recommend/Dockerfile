# Start with a Python image.
FROM python:3.6

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

# Copy all our files into the image.
WORKDIR /code
COPY . /code/

# Install our requirements.
RUN pip install -U pip
RUN pip install pipenv
RUN pipenv install --system --skip-lock

# Specify the command to run when the image is run.
RUN mkdir -p /opt/log/

CMD ["sh", "prod_run.sh"]