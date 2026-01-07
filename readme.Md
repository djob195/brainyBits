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

No Python installation is required locally.

---

## Docker Setup

### 1. Build the Docker Image

From the root of the repository:

```bash
docker-compose build
```

This will create a lightweight Python 3.11 container ready to run your code.