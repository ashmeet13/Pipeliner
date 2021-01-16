# Pipeliner
Figuring out the basics Data Pipelines.

## What is Pipeliner?
A pipelining sandbox is how I would put it.
Data pipelines can have several frameworks each serving a different use-case.
This project enables one to test those frameworks and understand the
basics for each of them.

## Included Frameworks
1. [Apache Superset](https://superset.apache.org/) - Data Visualization
2. [Apache Airflow](https://airflow.apache.org/) - Workflow Orchestration

## How does it work?

#### Understanding the repository structure

The current data source for testing these pipelines as of now is the `database` directory which basically does two things -
1. Start a PostgreSQL Database with a simple schema mimicing an Online E-Commerce Store
2. Start a Data Generator that will populate the PostgreSQL Database with artifical "orders".

Each framework will be defined in it's own directory. Each framework will also have a `Dockerfile` and `docker-compose.yaml` that can be used for easy setup and quick testing.

```
[airflow] - Will start the Airflow service and contain a simple DAG for reporting
[superset] - Will start the Superset service that can be used for Data Visualization
[database] - The data source and data generator to test out the frameworks
```

## Why?
Personally, I have two goals -
1. Having an easy setup for myself to simply test a framework that I come across when I a either read about it or hear someone talk about it.
2. I wish to improve my code quality and hence write better code that can be reused. I plan on doing this by -
	- Writing complete tests and for the simple pipelines that I write.
	- Making it easily accessible by Dockerizing it
	- Having a good documentation (Pending)
