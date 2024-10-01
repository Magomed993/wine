from http.server import HTTPServer, SimpleHTTPRequestHandler
import collections
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import argparse
from environs import Env


envi = Env()
envi.read_env()

def decline_years(n):
    if 11 <= n % 100 <= 19:
        return 'лет'
    else:
        remainde = n % 10
        if remainde == 1:
            return 'год'
        elif 2 <= remainde <= 4:
            return 'года'
        else:
            return 'лет'


if __name__ == '__main__':
    wines = envi.str('WINES')
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    now_date = datetime.date.today()
    start_work = 1920
    years_work = now_date.year - start_work

    parser = argparse.ArgumentParser(description='Если ваш файл находится не в папке с кодом, то вы можете ввести путь к нему дополнительным аргументом')
    parser.add_argument('--path', default=wines, help='Путь')
    args = parser.parse_args()

    wines_excel = pandas.read_excel(args.path,
                                    sheet_name='Лист1',
                                    na_values=['N/A', 'NA'],
                                    keep_default_na=False).to_dict(orient='records')
    wine_collection = collections.defaultdict(list)
    for wine in wines_excel:
        wine_collection[wine['Категория']].append(wine)

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
