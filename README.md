`Python` `Django` `Django Rest Framework` `Docker` `Gunicorn` `NGINX` `PostgreSQL`

# **_Foodgram_**
Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи публикуют свои рецепты, подписываются на публикации других пользователей, добавляют понравившиеся рецепты в список «Избранное», а перед походом в магазин могут скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
**_Ссылка на [проект](https://akshan3000.ddns.net/ "Гиперссылка к проекту.")_**
**_Ссылка на [админ-зону](https://akshan3000.ddns.net/admin "Гиперссылка к админке.")_**
**_Ссылка на документацию к [API](https://akshan3000.ddns.net//api/docs/ "Гиперссылка к API.") с актуальными адресами. Здесь описана структура возможных запросы и ожидаемых ответов_**

### _Развернуть проект на удаленном сервере:_

**_Клонировать репозиторий:_**
```
git clone git@github.com:OlegMusatov3000/foodgram-project-react.git
```
**_Установить на сервере Docker, Docker Compose:_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```

**_Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:_**
```
DOCKER_PASSWORD         - пароль от Docker Hub
DOCKER_USERNAME         - логин Docker Hub
HOST                    - публичный IP сервера
USER                    - имя пользователя на сервере
SSH_PASSPHRASE             - *если ssh-ключ защищен паролем
SSH_KEY                 - приватный ssh-ключ
TELEGRAM_TO             - ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          - токен бота, посылающего сообщение
```

**_Для ручной остановки контейнеров Docker выполните:_**
```
sudo docker compose down -v      - с их удалением
sudo docker compose stop         - без удаления
```
### После каждого обновления репозитория (push в ветку master) будет происходить:

1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
2. Сборка и доставка докер-образов frontend и backend на Docker Hub
3. Разворачивание проекта на удаленном сервере
4. Отправка сообщения в Telegram в случае успеха

### Автор
Олег Мусатов
### Telegram
@OlegMusatov