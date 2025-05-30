FROM python:3.11.12-bullseye

WORKDIR /

COPY requirements.txt .
COPY musicbot/ ./musicbot/

# Install OpenJDK 21
RUN apt update && \
    apt install -y wget && \
    wget https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.deb && \
    apt-get install -y ./jdk-21_linux-x64_bin.deb && \
    rm jdk-21_linux-x64_bin.deb && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "musicbot"]