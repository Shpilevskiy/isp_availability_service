### Description

ISP Service is a service that helps to gather data about high-speed internet connection availability in one place. It collects data about Ethernet and XPON tarrifs, converts it into single format and allows to check in the single form

### What it is made of
It is a bunch of python services built in top of Docker and Docker-Dompose.

#### Project structure:
```
.
+─── bin (a set of useful scripts)
│   └───fill_db.py (used to fill database with connections data without the need to launch celery tasks and wait for them to finish)
│   └───streets_to_text.py (used to put a list of all streets after validations in a text file for further analysis)
└─── falcon_microservice (contains Falcon API talking to database)
│
└─── nginx_microservice (contains nginx instance that serves static files)
│
└─── parser_routines (contains celery tasks responsible for parsing data from providers' sites. Briefly there is a Celery Beat Scheduler instance and 4 Celery workers that a launched on a daily basis)
```

### How Do I Launch it

1. Make sure you have docker installed and its daemon running.
2. Clone this repo (```git clone https://github.com/MrLokans/isp_availability_service```)
3. Go to project's root (```cd isp_availability_service```)
4. Launch database container (```docker-compose up -d db```)
5. Populate database data via running ```python bin/fill_db.py -d``` (this may take lots of time)
6. Stop running db instance (```docker-compose stop db```)
7. Launch all services via running (```docker-compose up --build```), it will take a lot of time during the first run to download all required images and build containers
8. You may visit http://127.0.0.1:8080 to see the results.