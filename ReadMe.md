This app predicts the outcome of future v75 (https://www.atg.se/spel/V75) trotting races, using a hyper-parameter tuned random forest model built on historical race data.  Not currently updated because the data site keeps changing tags, therefore making scraping harder.

Instructions: <br />
Install dependencies:   <br />
   &emsp; python3 -m pip install -r requirements.txt <br />
Run Docker container:  <br />
    &emsp; docker-compose up <br />
With running docker container, create database 'trav' in docker container postgres database <br />
    &emsp; login to container shell:   <br />
        &emsp; &emsp; docker exec -it <pg_container_name> /bin/bash  <br />
    &emsp; login to postres:   <br />
       &emsp; &emsp; psql -U postgres   <br />
    &emsp; create datbase:   <br />
        &emsp; &emsp; create database trav;  <br />
    &emsp; then exit postgres and container shell  <br />
Import unzipped postgres dump into database:  <br />
    &emsp; docker exec -i <container name> /bin/bash -c "PGPASSWORD=postgres psql --username postgres  trav" < <local apath to unzipped dump.sql>  <br />

Run main.py to start program  <br />
