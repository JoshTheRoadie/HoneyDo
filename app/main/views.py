from datetime import datetime
from flask import abort, redirect, render_template, session, url_for
from . import main
from .. models import User
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())
