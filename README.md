# library project

### Installation

- Download redis server -> `docker run -t --name my_redis -p 6379:6379 redis:alpine`
- Install pipenv -> `brew install pipenv`
- Create environment and install requirements with pipenv -> `pipenv install`
- Run migrations -> `pipenv run python3 manage.py migrate`
- Run server -> `pipenv run python3 manage.py runserver 0.0.0.0:8000`
