# -*- coding: utf-8 -*-
#==================================================
#	Project Name: server
#	File Name	: __init__.py
#	Author		: HuangDaTian
#	Create Time	: 2022-03-13  9:26:07
#	Modify Time	: 2022-03-13  9:26:07
#	Description	: 
#==================================================*/

from flask import Flask
from server import configs

app = Flask(__name__)
app.config.from_object(configs)

from server.viewIndex import indexBp
app.register_blueprint(indexBp)

