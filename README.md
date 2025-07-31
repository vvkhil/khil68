### 1. Клонирование проекта
```bash
git clone git@github.com:vvkhil/khil68.git
cd khil68
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных MySQL
Создать базу данных:
```sql
CREATE DATABASE json_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Настроить доступ в project/settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'json_project',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Применить миграции:

```bash
python manage.py migrate
```
⚙️ Настройка uWSGI и Nginx
uWSGI конфигурация
Файл: /etc/uwsgi/sites/json_project.ini

```ini
[uwsgi]
chdir = /home/vvkhil/json_project
module = project.wsgi:application
home = /home/vvkhil/json_project/venv

master = true
processes = 5

socket = /run/uwsgi/json_project.sock
chmod-socket = 660
vacuum = true

logto = /var/log/uwsgi/json_project.log
```
Systemd unit
Файл: /etc/systemd/system/uwsgi.service

```ini
[Unit]
Description=uWSGI instance to serve json_project
After=network.target

[Service]
User=vvkhil
Group=www-data
WorkingDirectory=/home/vvkhil/json_project
ExecStart=/home/vvkhil/json_project/venv/bin/uwsgi --ini /etc/uwsgi/sites/json_project.ini

[Install]
WantedBy=multi-user.target
```  
Перезапуск:

```bash
sudo systemctl daemon-reload
sudo systemctl restart uwsgi
sudo systemctl enable uwsgi
```
Nginx конфигурация
Файл: /etc/nginx/sites-available/json_project

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/json_project.sock;
    }

    location /static/ {
        alias /home/vvkhil/json_project/static/;
    }
}
```
Активировать сайт:

```bash
sudo ln -s /etc/nginx/sites-available/json_project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```
✅ Проверка работы
Перейти в браузере на http://localhost

Загрузить JSON-файл с данными

Проверить таблицу с данными на отдельной странице
