#!/usr/bin/env bash

# Скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Postgres позволяет подключиться к удаленной базе указав ссылку на нее после флага -d
# ссылка подгрузится из переменной окружения, 
# дальше мы загружаем в поключенную базу sql-файл с таблицами
make install && psql -a -d $DATABASE_URL -f database.sql