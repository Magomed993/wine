from http.server import HTTPServer, SimpleHTTPRequestHandler
from math import remainder

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from pprint import pprint

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

now_date = datetime.date.today()
start_work = 1920
years_work = now_date.year - start_work

def decline_years(n):
    if 11 <= n % 100 <= 19:
        return 'лет'
    else:
        remainde = n % 100
        if remainde == 1:
            return 'год'
        elif 2 <= remainde <= 4:
            return 'года'
        else:
            return 'лет'

excel_data_if = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)
excel_data_if_dict = excel_data_if.to_dict(orient='records')

excel_data_if_dict2 = pandas.read_excel('wine2.xlsx',
                                        sheet_name='Лист1',
                                        na_values=['N/A', 'NA'],
                                        keep_default_na=False).to_dict(orient='records')
wine_collection = collections.defaultdict(list)
for index in excel_data_if_dict2:
    wine_collection[index['Категория']].append(index)

rendered_page = template.render(
    current_year=years_work,
    word_year=decline_years(years_work),
    wines=wine_collection,
    name_collections=wine_collection.keys()
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
