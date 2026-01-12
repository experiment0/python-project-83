# Анализатор страниц

## Статусы

[![Actions Status](https://github.com/experiment0/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/experiment0/python-project-83/actions)
[![Python CI](https://github.com/experiment0/python-project-83/actions/workflows/python-ci.yml/badge.svg)](https://github.com/experiment0/python-project-83/actions/workflows/python-ci.yml)

## О проекте

> Проект находится в стадии реализации.

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

    # Локально запустить сервер
    make dev
   ```
   
   Перейти по ссылке http://127.0.0.1:5000

## Демонстрация работы

Проект также развернут на платформе `render.com`: \
https://python-project-83-jgqi.onrender.com/