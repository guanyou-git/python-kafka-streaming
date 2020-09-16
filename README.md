# Project Initialization Guide

To inspect the location of docker volume, you may run the following command

```bash
$docker volume ls
$docker volume inspect workspace_scripts_datastore
```

Take note of the "Mountpoint", copy the directory location, and migrate base validation_scripts into docker volume store

```bash
$cp -r ./validation_store/* <SPECIFY MOUNTPOINT HERE>/
```

