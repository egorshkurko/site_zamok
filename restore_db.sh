#!/bin/bash
# Скрипт для восстановления базы данных из бэкапа

cd /root/site_zamok_git

# Показываем список доступных бэкапов
echo "Доступные бэкапы:"
ls -lt db_backup_*.sqlite3 2>/dev/null | head -10

if [ $# -eq 0 ]; then
    echo ""
    echo "Использование: $0 <имя_бэкапа>"
    echo "Пример: $0 db_backup_20241124_150000.sqlite3"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Ошибка: файл $BACKUP_FILE не найден"
    exit 1
fi

# Останавливаем Gunicorn перед восстановлением
echo "Останавливаем Gunicorn..."
sudo systemctl stop gunicorn

# Создаем резервную копию текущей базы
CURRENT_BACKUP="db_before_restore_$(date '+%Y%m%d_%H%M%S').sqlite3"
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 "$CURRENT_BACKUP"
    echo "Текущая база сохранена как: $CURRENT_BACKUP"
fi

# Восстанавливаем базу
echo "Восстанавливаем базу из $BACKUP_FILE..."
cp "$BACKUP_FILE" db.sqlite3

# Запускаем Gunicorn обратно
echo "Запускаем Gunicorn..."
sudo systemctl start gunicorn

echo "База данных восстановлена из $BACKUP_FILE"

