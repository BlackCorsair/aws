#!/bin/bash
source /opt/s3upload/venv/bin/activate
/opt/s3upload/mysql-s3-backup.py # put here your options
/opt/s3upload/postgres-s3-backup.py # put here your options
rm -rf /tmp/*.sql.gz