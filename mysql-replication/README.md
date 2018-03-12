# Mysql Replication

The goal of this ansible role, is to provide the tools so a secondary instance of mysql starts at a given hour, replicate with the master node and then shutdowns itself after the replication is done.

## How to use it

```
ansible-playbook -i inventory replication.yml
```

Where:
* **inventory:** contains the machines
* **replication.yml:** is the ansible role itself

## What's working and what's not
* The role still needs an initial test, althought the replication.py script is mostly tested

## Implementing
* Ansible will check if the primary DB is alive to decide if start the instance or not.