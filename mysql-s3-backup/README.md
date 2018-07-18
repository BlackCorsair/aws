# MySQL S3 Backup
## What does this role do?
This Ansible Role backups the specified MySQL database in a S3 bucket.

## How to use it?
Modify the variables:
* **database**
* **dbadmin**
* **dbpass**
* **dbtype**
* **node** _(optional)_
* **bucket** 
* **object** 

And modify the inventory to fill your needs and then run the role from another playbook (in the example we asume it's named role-mysql-s3-backup.yml)
```
ansible-playbook role-mysql-s3-backup.ym
```

This is how the playbook could look:

```
---
# this playbooks launches the mysql-s3-backup role
- hosts: all
  become: true
  vars:
    database: "mydb"
    s3-backup: "s3-id"
  roles:
    - include: mysql-s3-backup 
```