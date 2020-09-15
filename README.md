# Quick notes

This is a very simple Python application we'll use to deploy in a VM.


# How to run the web application

To run this in development mode, use this command:
`FLASK_APP=flaskapp FLASK_ENV=development flask run`


# Connecting to the database
You can connect to the local postgres instance using these credentials:

```
username: <your username>
password: LE_SE_password
```

Using psql: `PGPASSWORD=LE_SE_password psql -U <your username> -h localhost`

# Endpoints

There are four endpoints in this web app, 3 of them should always return a 200 status code when you're properly connected to the database, and one should return an error all the time.

`/` -> The root endpoint that returns a JSON with the message `It works!`.

`/error` -> An endpoint that always raises an Internal Server Error.

`/logs` -> An endpoint that reads the visitor logs from the last 24 hours.

`/logs_write` -> An endpoint that records the user's browser and fake IP address. It then writes this to the database.