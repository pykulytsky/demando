# demando
Application for questions ,answers and voting

## Run with Docker
1. Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) on your local machine.
2. Clone this repository
```bash
git clone https://github.com/pykulytsky/demando.git
```
3. Go to directory with our project
```bash
cd demando
```
4. Build docekr image
```bash
docker-compose build app
```
5. Run docker compose
```bash
docker-compose up
```
---
## Run with uvicorn
1. Clone this repository
```bash
git clone https://github.com/pykulytsky/demando.git
```
2. Go to directory with our project
```bash
cd demando
```
3. Run uvicorn server
```bash
uvicorn --app-dir src/ main:app --workers 4
```
