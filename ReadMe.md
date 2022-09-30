This app predicts the outcome of future v75 (https://www.atg.se/spel/V75) trotting races, using a hyper-parameter tuned random forest model built on historical race data.

Instructions:
Install dependencies:
    python3 -m pip install -r requirements.txt to insta
Run Docker container:
    docker-compose up
With running docker container, create database 'trav' in docker container postgres database
    login to container shell:
        docker exec -it <pg_container_name> /bin/bash
    login to postres:
        psql -U postgres
    create datbase:
        create database trav;
    then exit container shell
Import unzipped postgres dump into database:
    docker exec -i <container name> /bin/bash -c "PGPASSWORD=postgres psql --username postgres  testing" < <local apath to unzipped dump.sql>

Run main.py to start program