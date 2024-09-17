# Overview
*Owner: Maycon Vinicius Guimarães*

This project involves setting up a data pipeline using Airflow to fetch data from the Open Brewery DB API, transform it, and store it in a data lake following the medallion architecture (Bronze, Silver, and Gold layers). The project is containerized using Docker.


# Prerequisites
- Docker
- Docker Compose
- Git

# Project Structure

```bash
breweries-pipeline/
├── dags/
│   └── breweries_dag.py      # The main DAG for the data pipeline
├── data/
│   └── bronze/     # Bronze Layer directory
│   └── silver/     # Silver Layer directory
│   └── gold/       # Gold Layer directory
├── docker-compose.yml       
├── Dockerfile
└── README.md
``` 

# Setup

### Clone reporsitory

```bash
git clone git@github.com:TheGuima/BreweriesPipeline.git
cd BreweriesPipeline
```

### Build airflow container
```bash
docker-compose up -d

# If it's the first time running it, run this code to setup the Postgres Database
docker-compose run --rm airflow-init

```
### Acess Airflow

Now you can access airflow *http://localhost:8080*

*Login:* Admin
*Password:* Admin

After that you just use the interface to run the dag *breweries_pipeline*
In the structure we mentioned above, you be able to see the results on *da* folder