# calculator-app

Add users, visualize their income and employment history, project future income, and conduct calculations on their data.


## Table of contents

* [Demo](#demo)
* [Structure](#structure)
* [Important notes](#important-notes)
* [How to run this app](#how-to-run-this-app)
* [Backend endpoints - Django](#backend-endpoints---django)
* [Available pages - React](#available-pages---react)
* [Extra](#extra)

## Demo

## Structure

- `api` - contains Django app files
- `frontend` - contains React app files
- `tools` - contains configuration files (environment settings and Dockerfile)

## Important Notes

1. Until the admin sets the Argyle API keys (`/api-keys/`), adding new Argyle user will be not possible.

## How to run this app?

### 1. Set all environment variables

Go to the `tools/env` directory, create a new `.env` file inside, and copy the contents of the `.env.example` file
into `.env`. Fill in all empty attributes values.

### 2. Set database credentials in the docker-compose.yml file

```  
db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: <postgres_user>
      POSTGRES_PASSWORD: <postgress_password>
      POSTGRES_DB: <database_name>
```

### 3. Build and run backend app

#### Docker

```
# build and run backend project
cd calculator-app
docker-compose up -d
docker-compose logs -tf

# create admin
docker-compose exec api python manage.py createsuperuser

# run frontend
cd frontend
npm install
npm start
```

#### Docker + Makefile

```
make build
make createsuperuser
make run
```

## Backend endpoints - Django

`/admin/*` - Django admin pages \
`/auth/*` - authentication endpoints \
`/admin-users/*` - endpoints for creating/activating/deleting admin users \
`/users/*` - responsible for fetching argyle user data, incomes, employment history, preparing collection of statistics \
`/integrations/*` - endpoints allow setting/displaying Argyle API keys

## Available pages - React

`/` - Homepage - available for everyone \
`/auth/login/` - the admin login page \
`/auth/password-reset/` - the admin password reset page \
`/auth/activate/:admin_user_id` - the admin activation 

* Admin List (`/accounts/`) - the list of all admins, allows to add a new one or deactivate existing.
* API (`/api-keys/`) - set Argyle credentials
* User List (`/users/`) - the list of users with opportunity to see detailed data, visualize their income and employment
  history, project future income
* User Details (`/details/:argyle_id`) - the Argyle user details, income visualization, employment history, future
  income projection
* Logout (`/auth/logout/`) - logout

## Extra

### Makefile

Run project

```
make / make run
```

Build project

```
make build
```

Stop project

```
make stop
```

Logs

```
make logs
```

Make migrations

```
make makemigrations
```

Migration

```
make migrate
```

Reset db

```
make reset-db
```

CLI

```
make cli
```

Creating new app in apps folder

```
make app app_name=<app_name>
```

Creating superuser

```make app app_name=<app_name>
make createsuperuser
```