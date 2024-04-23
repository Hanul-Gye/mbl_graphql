FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# requirements.txt만 먼저 복사하여 의존성 설치
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Django 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]