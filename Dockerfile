FROM python:3.11-slim-bookworm

WORKDIR /userbot

ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1

# catub/core:bullseye is Python 3.9. wikipedia and current yt-dlp require 3.11.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    ffmpeg \
    gcc \
    git \
    libffi-dev \
    libjpeg62-turbo-dev \
    libmagickwand-dev \
    libpq-dev \
    libwebp-dev \
    mediainfo \
    unzip \
    wget \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV PATH="/userbot/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "userbot"]
