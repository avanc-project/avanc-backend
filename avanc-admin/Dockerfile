FROM python:3.9

WORKDIR /

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY . .


# Установите зависимости
RUN  pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" && gunicorn --bind 0.0.0.0:8000 config.wsgi