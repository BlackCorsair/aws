#!/bin/bash
source /opt/s3upload/venv/bin/activate
/opt/s3upload/mysql-s3-backup.py
/opt/s3upload/postgres-s3-backup.py
rm -rf /tmp/*.sql.gz