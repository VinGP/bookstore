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

#### 3) переименовываем файлы:

*.env.dev.example* -> *.env* \
*docker-compose.dev.yml* -> *docker-compose.yml*

#### 4) Поднимаем контейнер

```shell
docker-compose up --build -d
```

или с помощью make

```shell
make dev
```

### Запуск проекта на сервере:

#### 1) Клонируем репозиторий

```shell
git clone https://github.com/Badsnus/QuizGame.git
```

#### 2)Заходим в директорию репозитория

```shell
cd bookstore
```

#### 3) переименовываем файл *.env.prod.example* в *.env*

*.env.prod.example* -> *.env* \
*docker-compose.prod.yml* -> *docker-compose.yml*

#### 4) Поднимаем контейнер

```shell
docker-compose up --build -d
```

или с помощью make

```shell
make up
```
