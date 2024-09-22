from http.server import HTTPServer, SimpleHTTPRequestHandler
from math import remainder

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

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

rendered_page = template.render(
    current_year=years_work,
    word_year=decline_years(years_work),
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
