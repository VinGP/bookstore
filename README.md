## Запуск проекта

___

### Запуск проекта локально:

#### 1) Клонируем репозиторий

```shell
git clone https://github.com/Badsnus/QuizGame.git
```

#### 2)Заходим в директорию репозитория

```shell
    cd bookstore
```

#### 3) переименовываем файл *.env.dev.example* в *.env*

#### 4) Поднимаем контейнер

```shell
docker-compose up --build -d
docker-compose exec web python manage.py create_db
```

или с помощью make

```shell
make dev create-db
```

### Запуск проекта для разработки:

#### 1) Клонируем репозиторий

```shell
git clone https://github.com/Badsnus/QuizGame.git
```

#### 2)Заходим в директорию репозитория

```shell
    cd bookstore
```

#### 3) переименовываем файл *.env.prod.example* в *.env*

#### 4) Поднимаем контейнер

```shell
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose exec web python manage.py create_db
```

или с помощью make

```shell
make prod create-db
```
