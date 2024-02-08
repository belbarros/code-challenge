
# Lighthouse Code Challenge

This is my resolution for the Lighthouse Code Challenge. This is the Data Engineering challenge, where you're supposed to build a pipeline that extracts data from two different sources and write the data to your local disc first, and to a PostgresSQL database afterwards.

## Tools used

For this challenge I used [Meltano](https://meltano.com/), [Apache Airflow](https://airflow.apache.org/), [PostgresSQL](https://www.postgresql.org/) and [Docker](https://www.docker.com/). 

## Installation
1. Clone this repository
2. Start a [virtualenv](https://virtualenv.pypa.io/en/latest/index.html)
```bash
python -m venv env_name
source env_name/bin/activate
```
2. Run the two docker-compose located in the root file on your venv.
3. Install the tools necessary:

```bash
pip install meltano apache-airflow
```

## The project

The first step on this project was the set-up of the extractors (tap) and loaders (target) - the tools used for the extraction and loading of the data. This project has three pipelines, each set up on a separate file.

The first pipeline is where the CSV file provided is extracted and loaded into a local disk. I used the [tap-csv](https://hub.meltano.com/extractors/tap-csv/) to extract the data and [target-csv](https://hub.meltano.com/loaders/target-csv) to save it locally as a CSV file. I chose the CSV file extension so I would not need to work with too many different types of taps/loaders, making the project less complex overall.

The second one is where we extract the PostgreSQL data and loaded into a local disk. I used the [tap-postgres](https://hub.meltano.com/extractors/tap-postgres/) paired with the target-csv loader.

This step presented a few challenges.
First, I needed to organize the extracted data into folders for each table. The solution I decided on was creating a separate pair of tap-target for each table. This was the best workaround for my situation given my level of expertise with the tool, since it not only resolved the folder situation, but also made my resolution of the next step easier, given the tools I selected and knew how to use.

<img src='/img/tap.png' />


After that, in some of the tables there was data in decimal format, and they were not being accepted by the loader. The solution for this was setting up a mapper. The mapper chosen was the [meltano-map-transformer](https://hub.meltano.com/mappers/meltano-map-transformer/), and what it does is transform the decimals on those tables into strings.

<img src='/img/mapper.png' />


The third and last pipeline is getting the CSV files on my local disk and sending them to the PostgreSQL database. I used the tap-csv and the [target-postgres](https://hub.meltano.com/loaders/target-postgres). I chose this setup so I could get the primary keys needed for this tap separately and correctly and also make sure it was always getting all the data extracted previously.

And this is how the end database is looking!

<img src='/img/db.png' />


After the pipelines were set up, it was time to code the DAG file, where we do the integration and scheduling with Airflow.

<img src='/img/airflow.png' />

I first tried implementing a variable python function, where we have the task_id and the name of the meltano job corresponding to each task utilizing a DockerOperator to run an image of Meltano where we're going to call our pipeline jobs. But I ran with an issue of connectivity and permissions for the docker + airflow that none of the solutions I found online or was suggested to try worked. This is one of the error messages I got through Airflow:
```
docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
[2024-02-07, 19:38:33 UTC] {taskinstance.py:1138} INFO - Marking task as FAILED. dag_id=lighthouse_challenge, task_id=extracts.docker_command, execution_date=20240207T193830, start_date=20240207T193833, end_date=20240207T193833
[2024-02-07, 19:38:33 UTC] {standard_task_runner.py:107} ERROR - Failed to execute job 35 for task extracts.docker_command (Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied')); 60)
[2024-02-07, 19:38:33 UTC] {local_task_job_runner.py:234} INFO - Task exited with return code 1
[2024-02-07, 19:38:33 UTC] {taskinstance.py:3280} INFO - 0 downstream tasks scheduled from follow-on schedule check
```

I believe this is the best possible solution, but for technical issues it wasn't working. This is a known problem, documented by users as we can see [here](https://github.com/docker/for-mac/issues/4755) and [here](https://www.reddit.com/r/dataengineering/comments/kmojyc/how_can_i_used_the_dockeroperator_in_airflow_of_i/), for example. I tried all I could find and nothing worked for me.

I also tried using BashOperator.
For the bash I tried creating a custom Dockerfile so the bash_command could work and do the meltano run job, but there was a conflict between versions of the Airflow and Meltano, so it made the installations very complicated, and in the end it didn't work.

<img src='/img/dockerfile.png' />


## Conclusion
This project was no short of challenges! I had a lot of hours dedicated to it, reading the documentations, trial and error, friends from the field to give me tips (I love you guys!), Google and Stackoverflow searches, and I learned so much! I'm now very prepared and very excited for all the new challenges Lighthouse will bring me. :smile: