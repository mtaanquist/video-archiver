FROM debian:bookworm

ENV FFMPEG_DIR=/usr/local/bin
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    xz-utils \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install the latest stable ffmpeg static build
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    -o /tmp/ffmpeg-release-amd64-static.tar.xz && \
    tar -xJf /tmp/ffmpeg-release-amd64-static.tar.xz -C /tmp && \
    mv /tmp/ffmpeg-*-amd64-static/ffmpeg /tmp/ffmpeg-*-amd64-static/ffprobe $FFMPEG_DIR && \
    chmod +x $FFMPEG_DIR/ffmpeg $FFMPEG_DIR/ffprobe && \
    rm -rf /tmp/ffmpeg-*

# Verify that we have ffmpeg installed
RUN ffmpeg -version

WORKDIR /app

# We need a virtual environment to install the Python dependencies
# due to the fact we installed Python3 via apt-get
RUN python3 -m venv /opt/venv

COPY ./app /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
