# demando
Application for questions ,answers and voting

## Run using Docker
1.
```bash
git clone https://github.com/pykulytsky/demando.git
```
2.
```bash
cd demando
```
3.
```bash
docker-compose build app
```
4.
```bash
docker-compose up
```
---
## Run using uvicorn
1.
```bash
git clone https://github.com/pykulytsky/demando.git
```
2.
```bash
cd demando
```
3.
```bash
uvicorn --app-dir src/ main:app --workers 4
```
