# app/tasks.py
from flask import Blueprint, render_template, request, redirect, url_for, g
lessonPage = Blueprint('lessons', __name__, url_prefix="/lessons")
from ..module import tasks
import json
from pathlib import Path

tasks_dir = Path(__file__).parent.parent / "site" / "tasks"



@lessonPage.route('/')
def main():
    return render_template("user/lessions.html", tasks=tasks.getTasks())

@lessonPage.route("/<int:id>")
def get_task(id):
    file = tasks_dir.joinpath(str(id)+".json")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return render_template("tests/templates/code.html", data=data)

