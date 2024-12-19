import os
import subprocess

# Step 1: Define Dockerfile content
dockerfile_content = """
FROM python:3.10.6
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && \
    apt -qq install -y git wget pv jq python3-dev ffmpeg mediainfo neofetch && \
    apt-get install wget -y -f && \
    apt-get install fontconfig -y -f

COPY . .
RUN pip3 install -r requirements.txt
CMD gunicorn app:app & python3 bot.py
"""

# Step 2: Write Dockerfile
dockerfile_path = "Dockerfile"
with open(dockerfile_path, "w") as dockerfile:
    dockerfile.write(dockerfile_content)

print(f"Dockerfile created at {os.path.abspath(dockerfile_path)}")

# Step 3: Build the Docker image
try:
    print("Building the Docker image...")
    subprocess.run(["docker", "build", ".", "-t", "hetlr"], check=True)
    print("Docker image 'hetlr' built successfully.")
except subprocess.CalledProcessError as e:
    print("Error during Docker image build:", e)
    exit(1)

# Step 4: Run the Docker container
try:
    print("Running the Docker container...")
    subprocess.run(["docker", "run", "-p", "80:80", "-p", "8080:8080", "hetlr"], check=True)
    print("Docker container is running.")
except subprocess.CalledProcessError as e:
    print("Error during Docker container run:", e)
    exit(1)
