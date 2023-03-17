## Запуск проекта

___

### Запуск проекта локально:

#### 1) Клонируем репозиторий

```shell
git clone https://github.com/VinGP/bookstore.git
```

#### 2)Заходим в директорию репозитория

```shell
cd bookstore
```

#### 3) Редактируем файлы

1. переименовываем файл *.env.dev.example* -> *.env*
2. Редактируем переменные в файле *.env* (по желанию)
    - Вместо MailHog вы можете подключить свою электронную почту, например Gmail:
        - MAIL_SERVER = smtp.gmail.com
        - MAIL_PORT = 587
        - MAIL_USE_TLS = true
        - MAIL_USERNAME = адрес (example@gmail.com)
        - MAIL_PASSWORD = пароль

#### 4) Поднимаем контейнер

```shell
docker-compose up --build -d
```

или с помощью make

```shell
make dev
```

#### 5) Применяем миграции

```shell
docker-compose exec web python -m alembic upgrade head
```

#### Для разработки:

После выполнения пунктов для локального запуска, надо выполнить следующие команды:

```shell
python -m venv venv
.\venv\Scripts\activate    
pip install -r bookstore/requirements-dev.txt
pre-commit install 
```

По итогу у вас должны заработать следующие сервисы:

- Bookstore
    - http://localhost:5000 - Основное приложение
    - http://localhost:5000/admin - Панель администрации
- MailHog (Для тестирования отправки почты)
    - http://localhost:8025/ - веб интерфейс
    - http://localhost:1025/ - SMTP сервер
- Postgresql
    - http://localhost:54320/ - База данных приложения (54320 - для локального
      подключения; 5432 - внутри контейнеров)
    - http://localhost:5050/ - pgAdmin для администрирования базы данных (email:
      admin@admin.com; пароль: root)

### Запуск проекта на сервере:

___

#### 1) Клонируем репозиторий

```shell
git clone https://github.com/VinGP/bookstore.git
```

#### 2)Заходим в директорию репозитория

```shell
cd bookstore
```

#### 3) Редактируем файлы

1. переименовываем файл *.env.prod.example* -> *.env*
2. удаляем файл *docker-compose.yml*
3. переименовываем файл *docker-compose.prod.yml* -> *docker-compose.yml*
4. Редактируем переменные в файле *.env*

#### 4) Поднимаем контейнер

```shell
docker-compose up --build -d
```

или с помощью make

```shell
make up
```

#### 5) Применяем миграции

```shell
docker-compose exec web python -m alembic upgrade head
```

### Запуск проекта на сервере c SSL сертификатом:

В проекте использовался бесплатный сертификат от Let’s Encrypt. Для этого вам надо приобрести доменное имя, делать DNS-записи типа A со значениями:
- @ - your_ip
- www - your_ip

#### 1) Клонируем репозиторий

```shell
git clone https://github.com/VinGP/bookstore.git
```

#### 2)Заходим в директорию репозитория

```shell
cd bookstore
```

#### 3) Редактируем файлы

1. переименовываем файл *.env.prod.ssl.example* -> *.env*
2. удаляем файл *docker-compose.yml*
3. переименовываем файл *docker-compose.prod.ssl.yml* -> *docker-compose.yml*
4. Редактируем переменные в файле *.env*
    - DOMAIN - ваш домен (example.org)
    - DOMAIN_WWW - домен третьего уровня (www.example.org)
    - EMAIL - адрес электронной почты для сертификата

#### 4) Получаем сертификаты:

```shell
bash init-letsencrypt.sh
```

#### 5) Поднимаем контейнер

```shell
docker-compose up --build -d
```

#### 6) Применяем миграции

```shell
docker-compose exec web python -m alembic upgrade head
```