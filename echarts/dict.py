import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
# from data import data

import json

with open("data.json") as json_file:
        config = json.load(json_file)
        print(config["data"]["dayList"])


