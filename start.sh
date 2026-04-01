#!/bin/bash
export PORT=5000
unset PIP_USER

# Создаём venv, если его нет
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активируем venv
source venv/bin/activate

# Обновляем pip
python -m pip install --upgrade pip

# Устанавливаем зависимости
pip install --no-cache-dir -r requirements.txt

# Запуск приложения
python main.py