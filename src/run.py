#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run server script."""

from flask import Flask
from src.apis.routes import app_v1
from src.config import Configurations as Config


app = Flask(__name__)
config = Config()
app.secret_key = config.SECRET_KEY
app.register_blueprint(app_v1)
