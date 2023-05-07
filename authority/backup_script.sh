#!/bin/bash

# Set variables
USERNAME="your_username"
DB_NAME="your_database_name"
BACKUP_DIR="/path/to/backup/directory"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup the database to a text file
pg_dump -U $USERNAME -W -F plain -f "${BACKUP_DIR}/backup_${TIMESTAMP}.sql" $DB_NAME

# Optional: Remove backups older than 30 days
find $BACKUP_DIR -type f -name "*.sql" -mtime +30 -exec rm {} \;


# mysqldump -u your_username -p your_database_name > backup.sql
# mysql -u your_username -p your_database_name < backup.sql

# chmod +x backup_script.sh

# crontab -e

# 0 * * * * /path/to/backup_script.sh
