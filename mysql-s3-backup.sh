#!/bin/bash
# This scripts has the following dependencies:
# awscli
# boto3
# to install them on rhel systems: yum install -y python-pip  && pip install awscli boto3
# to install them on debian systems: apt install -y python-pip  && pip install awscli boto3

# Variables

NODE="node1"
DATABASE=""
USER=""
PASS=""
BUCKET=""

# Variables END

# echoes the program usage
help() {
    echo "#######################"
    echo ""
    echo "This script has the following dependencies: awscli boto3"
    echo ""
    echo "#######################"

    echo ""
    echo "      How to use this script:"
    echo "      -h -> show this message"
    echo "      -n node -> sets the node name, by default the node is called node1"
    echo "      -d database -> specifies the database name"
    echo "      -u user -> specifies the database user"
    echo "      -p password -> specifies the database user password"
    echo "      -b bucket -> specifies the S3 bucket name"
    echo ""
    echo "@@@@ example @@@@"
    echo ""     
    echo "      mysql-s3-backup.sh -u root -p nein -n pre1 -d users -b db-backups -o dbs3.sql"
    echo ""
    echo "#######################"

}

# gets the variables from the parameters introduced while executing the script
getVariables () {
    if [ "$#" -gt "9" ]; then
        for i in $#
        do
            if [ "$i" = "-n" ]; then
                $NODE=$(i+1)
            elif [ "$i" = "-d" ]; then
                $DATABASE=$(i+1)
            elif [ "$i" = "-u" ]; then
                $USER=$(i+1)
            elif [ "$i" = "-p" ]; then
                $PASS=$(i+1)
            elif [ "$i" = "-b" ]; then
                $BUCKET=$(i+1)
            fi
        done    
    elif [ "$1" = "-h" ]; then
        help
    fi
}

# dumps the DB
dumpDB () {
    mysql -u$USER -p$PASS $DATABASE > /tmp/$(date %Y%m%d-%h%m-$DATABASE-$NODE).sql
}

# uploads the dump to the S3 bucket
uploadS3 () {
    aws s3 cp /tmp/$(date %Y%m%d-%h%m-$DATABASE-$NODE).sql s3:/$BUCKET/
}

getVariables
dumpDB
uploadS3