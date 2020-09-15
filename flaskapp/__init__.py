import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

from sqlalchemy.exc import SQLAlchemyError

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# envs
DB_USER = os.getenv("DATA_DB_USER")
DB_PASSWORD = os.getenv("DATA_DB_PASS")
DB_HOST = os.getenv("DATA_DB_HOST")
DB_NAME = os.getenv("DATA_DB_NAME")

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY="dev", SQLALCHEMY_TRACK_MODIFICATIONS=False)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy(app)


@dataclass
class ActivityLog(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    ip_addr: str = db.Column(db.String(80))
    browser: str = db.Column(db.String(120))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __iter__(self):
        return self.to_dict().iteritems()


try:
    db.create_all()
except SQLAlchemyError as e:
    logging.warning(f"Error creating the database: {e}")


# a simple page that says hello
@app.route("/")
def hello():
    return jsonify({"msg": "It works!"})


@app.route("/error")
def error():
    raise Exception("Uh oh! Somethng went wrong!")


@app.route("/logs")
def get_logs():
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    logs = ActivityLog.query.filter(ActivityLog.created_at >= one_day_ago).all()
    return jsonify([asdict(l) for l in logs])


@app.route("/logs_write")
def write_log():
    ip_addr = "xx.xx.xx.xx"
    log = ActivityLog(ip_addr=ip_addr, browser=request.user_agent.browser)
    db.session.add(log)
    db.session.commit()
    return jsonify({"msg": "Log write success!"})
