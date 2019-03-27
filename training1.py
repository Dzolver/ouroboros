import sqlite3
import json
from datetime import datetime

timeframe = '2015-05'
sql_transaction = []
connection = sqlite3.connect('{}.db'.format(timeframe))
cursor = connection.cursor()