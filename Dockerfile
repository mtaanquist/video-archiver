# Stage 1: Build ffmpeg in a separate stage to keep final image size small
FROM debian:buster AS ffmpeg-builder

# Install build dependencies for ffmpeg
RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    build-essential \
    cmake \
    git \
    libass-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libtheora-dev \
    libtool \
    libvorbis-dev \
    libx264-dev \
    libx265-dev \
    libvpx-dev \
    pkg-config \
    wget \
    yasm \
    && rm -rf /var/lib/apt/lists/*

# Clone ffmpeg sources
WORKDIR /ffmpeg_sources
RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg

# Build ffmpeg
WORKDIR /ffmpeg_sources/ffmpeg
RUN ./configure --prefix=/usr/local --disable-debug --disable-doc --disable-ffplay \
    --enable-gpl --enable-libx264 --enable-libx265 --enable-libvpx \
    --enable-nonfree \
    && make -j$(nproc) && make install && make distclean

# Stage 2: Setup the Python environment
FROM python:3.10-slim

# Copy the ffmpeg binaries from the builder stage
COPY --from=ffmpeg-builder /usr/local /usr/local

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Default command to run on container start
CMD ["python", "main.py"]
