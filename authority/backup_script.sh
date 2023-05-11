#!/bin/bash

# Set variables
USERNAME="sc20osc"
DB_NAME="sc20osc\$db"
BACKUP_DIR="/authority/backups/"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup the database to a text file
mysqldump -U $USERNAME -W -F plain -f "${BACKUP_DIR}/backup_${TIMESTAMP}.sql" $DB_NAME

# Optional: Remove backups older than 30 days
find $BACKUP_DIR -type f -name "*.sql" -mtime +30 -exec rm {} \;


# crontab -e
# 0 * * * * /path/to/backup_script.sh
