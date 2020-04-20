FROM richarddally/cpython:3.8.2_18.04

MAINTAINER r.dally@protonmail.com


# Install MongoDB
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > tee /etc/apt/sources.list.d/mongodb.list
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
ADD requirements.txt /app
RUN python3 -m pip install -r requirements.txt

ADD abstract_fetcher.py /app
ADD clean_price_test.py /app
ADD cpu_fetcher.py /app
ADD cpu_fetcher_test.py /app
ADD cybertek.py /app
ADD frontend.py /app
ADD grosbill.py /app
ADD hardwareshop.py /app
ADD ldlc.py /app
ADD materiel.py /app
ADD mindfactory.py /app
ADD nvidia_fetcher.py /app
ADD nvidia_fetcher_test.py /app
ADD pricedatabase.py /app
ADD publish.py /app
ADD rueducommerce.py /app
ADD setup.py /app
ADD source.py /app
ADD source_test.py /app
ADD toolbox.py /app
ADD topachat.py /app

ENTRYPOINT ["python3", "/app/cpu_fetcher.py"]