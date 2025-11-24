#!/bin/bash
# Скрипт для автоматического бэкапа базы данных в Git
# Создает копию базы с датой в имени, чтобы не перезаписывать локальную базу

cd /root/site_zamok_git

# Создаем копию базы данных с датой в имени
BACKUP_NAME="db_backup_$(date '+%Y%m%d_%H%M%S').sqlite3"
cp db.sqlite3 "$BACKUP_NAME"

# Добавляем бэкап в Git
git add "$BACKUP_NAME"

# Коммитим с датой и временем
COMMIT_MSG="Auto backup: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG" || exit 0  # Если изменений нет, выходим

# Пушим в репозиторий
git push origin main

# Удаляем старые бэкапы (оставляем только последние 10)
ls -t db_backup_*.sqlite3 2>/dev/null | tail -n +11 | xargs -r rm

echo "Backup completed: $BACKUP_NAME at $(date)"

