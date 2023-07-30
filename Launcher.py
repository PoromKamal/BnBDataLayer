from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
mysql = MySQL(app)

@app.route('/test')
def login():
    return "Hello World!"

if __name__ == '__main__':
  app.run(host="localhost", port=5000)