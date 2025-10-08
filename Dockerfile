FROM python:3.11-slim

# Встановлюємо python3 та pip, якщо ще нема, і створюємо посилання python -> python3
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -sf /usr/bin/python3 /usr/bin/python

# Встановлюємо залежності
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо все у контейнер
COPY . /code/

# Додаємо права на виконання для entrypoint
RUN chmod +x /code/entrypoint.sh

# Вказуємо скрипт як точку входу
ENTRYPOINT ["/code/entrypoint.sh"]

