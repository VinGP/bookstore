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
2. Редактируем переменные в файле *.env*

#### 4) Поднимаем контейнер

```shell
docker-compose up --build -d
```

или с помощью make

```shell
make dev
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
    - http://localhost:54320/ - База данных приложения (54320 - для локального подключения; 5432 - внутри контейнеров)
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
