FROM python:3.10
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl android-tools-adb iputils-ping
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "/app/main.py"]