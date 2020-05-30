FROM richarddally/cpython:3.8.2_18.04

# Install MongoDB
RUN echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" > /etc/apt/sources.list.d/mongodb.list
RUN apt-get update

# Install MongoDB package (.deb)
RUN apt-get install -y mongodb


# Define the volume
VOLUME ["/app/db"]

# Define the port
EXPOSE 3000

ENV MONGO_HOST "host.docker.internal"

# Create directory
RUN mkdir -p /app
WORKDIR /app


# Install requirements
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt

COPY *.py /app

ENTRYPOINT ["python3", "/app/cpu_fetcher.py"]
