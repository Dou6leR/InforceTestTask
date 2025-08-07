# Inforce Test Task
# Project Setup Commands

Below are the commands to set up and run the project using Docker Compose:

Clone the repository
```bash
git clone https://github.com/Dou6leR/InforceTestTask.git
cd InforceTestTask
```

Setting up the docker
```bash
docker compose up --build -d
```

Creating superuser
```bash
docker-compose exec -ti django python manage.py createsuperuser
```

Run all tests
```bash
docker compose exec django pytest
```

Install dependencies manually (for local non-Docker use) with:
```bash
pip install -r requirements.txt
```

Stop all containers:
```bash
docker compose down
```

Stop and remove everything including volumes:
```bash
docker compose down -v
```

Back end port
```bash
8000:8000
```

pgAdmin port
```bash
5050:80
```
