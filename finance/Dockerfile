FROM python:3.12-bookworm

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt 

RUN mkdir -p /.config/matplotlib \
    && chmod 777 -R /.config \
    && mkdir -p /.cache \
    && chmod 777 -R /.cache