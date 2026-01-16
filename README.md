# Анализатор страниц

## Статусы

### Статусы workflow actions

[![Actions Status](https://github.com/experiment0/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/experiment0/python-project-83/actions)
[![Python CI](https://github.com/experiment0/python-project-83/actions/workflows/python-ci.yml/badge.svg)](https://github.com/experiment0/python-project-83/actions/workflows/python-ci.yml)

### Статусы [SonarQube](https://sonarcloud.io/)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=bugs)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-83&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-83)

## О проекте

Данный проект создан в процессе прохождения курса [Python-разработчик](https://ru.hexlet.io/programs/python).\
В нем реализовано web-приложение на Flask для проверки доступности сайтов и анализа заполнения тегов, значимых для SEO.

## Демонстрация работы

Проект развернут на платформе [render.com](https://render.com/) и доступен по ссылке: \
https://python-project-83-jgqi.onrender.com/

> **Примечание.** \
> Поскольку для деплоя сайта используется бесплатный тариф, \
> платформа `render.com` утилизует ресурсы, которые не используются какое-то время.\
> Поэтому при открытии сайта, возможно, загрузка сайта начнется с процесса его сборки \
> и нужно будет подождать ее окончания.\
> Также на `render.com` довольно нестабильное соединение с БД.\
> В случае появления ошибок, нужно обновить страницу.

[Видео с демо работы сайта](https://disk.yandex.ru/i/j4X0FTNm-kY-CA)

## Инструкция по локальному запуску

1. Проверить, установлена ли утилита `uv`:

   ```sh
   uv --version
   ```

   Если не установлена, то нужно установить [по инструкции](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

2. Проверить, установлена ли утилита `make`:

   ```sh
   make --version
   ```

   Если не установлена, то установить [на windows](https://stackoverflow.com/questions/32127524/how-can-i-install-and-use-make-in-windows) или [на ubuntu](https://andreyex.ru/ubuntu/kak-ustanovit-make-na-ubuntu/).

3. ```sh
   # Клонировать проект
   git clone https://github.com/experiment0/python-project-83.git

   # Перейти в папку с проектом
   cd python-project-83

   # Установить зависимости
   make install
   ```

4. Создать в корне проекта файл `.env` для переменных среды.

   ```sh
   touch .env
   ```

   И добавить в него переменные среды по аналогии с образцом из файла [.env-example](./.env-example) \
   В переменной `DATABASE_URL` указывается путь для соединения с БД PostgreSQL. \
   Если она не установлена, ее нужно установить [по инструкции](https://tproger.ru/articles/osnovy-postgresql-dlya-nachinayushhih--ot-ustanovki-do-pervyh-zaprosov-250851).

5. ```sh
   # Запустить локальный сервер
   make dev
   ```
   Перейти по ссылке http://127.0.0.1:5000
