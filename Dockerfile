FROM catub/core:bullseye

# Working directory
WORKDIR /userbot

# Timezone
ENV TZ=Asia/Kolkata

## Copy files into the Docker image
COPY . .

ENV PATH="/home/userbot/bin:$PATH"

# catub/core:bullseye is Python 3.9. Pillow 12+ does not support 3.9.
# Install a 3.9-compatible Pillow first, then the rest of requirements.
RUN pip install --no-cache-dir "Pillow==10.4.0" \
&& grep -ivE '^[[:space:]]*Pillow' requirements.txt > /tmp/requirements.nopillow.txt \
&& pip install --no-cache-dir -r /tmp/requirements.nopillow.txt


CMD ["python3","-m","userbot"]