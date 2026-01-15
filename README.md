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

> Проект находится в стадии реализации.

## Демонстрация работы

Проект развернут на платформе `render.com`: \
https://python-project-83-jgqi.onrender.com/

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

3. 
    ```sh
    # Клонировать проект
    git clone https://github.com/experiment0/python-project-83.git

    # Перейти в папку с проектом
    cd python-project-83

    # Установить зависимости
    make install

    # Запустить локальный сервер
    make dev
   ```
   
   Перейти по ссылке http://127.0.0.1:5000
