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
