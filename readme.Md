# Python Structures Project

This repository contains Python implementations of various **data structures and algorithms** These implementations are inspired by the data structures discussed on my blog: [https://djob195.github.io](https://djob195.github.io).

The project is designed to be executed in a lightweight, reproducible environment using **Docker** and **Docker Compose**.


![Python Version](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Project Structure

```plaintext
root/
├── structures/             # Python projects
│   └── heap_project/       # Heap implementation
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
└── README.md
```

All code inside the `structures/` folder is automatically available inside the Docker container.

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

No local Python installation is required.

---

## Docker Setup

### 1. Build the Docker Image

From the root of the repository:

```bash
docker-compose build
```
This will create a lightweight Python 3.11 container called: **brainybits-python-enviroment**.

### 2. Start the Container

```bash
docker-compose up -d
```

The container runs in daemon mode (background). To ensure it is running correctly, you can verify it with the following command:

```bash
docker ps
```
This command will display a list of all running containers.

### 3. run a command inside a running containe

```bash
docker exec -it python-enviroment-container sh
```

> Note: if you use windows, does not forget command **winpty** before command `docker`.

After executing this command, you will be inside the container, within a Python environment. From there, you will be able to execute and explore all the projects included in this repository.