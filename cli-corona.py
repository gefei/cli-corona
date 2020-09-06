# IT License
#
# Copyright (c) 2020 Gefei gefei.zhang@pst.ifi.lmu.de
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
from bokeh.io import export_png
from bokeh.palettes import Category10

import pandas as pd

import itertools
from argparse import ArgumentParser

def color_gen():
    yield from itertools.cycle(Category10[10])

def plot_a_country(pic, df, country, daily, ave, per100k, color):
    df_country=df[df['id'] == country]
    df_country['dateRep'] = pd.to_datetime(df.date, format='%Y%m%d')

    tmp = df_country[['confirmed']]
    df_country['new'] = tmp.diff(periods=1,axis=0)
    if (per100k):
        df_country['new'] = df_country['new'] / df_country['population'] * 100000
    tmp = df_country[['new']]
    tmp.ave = tmp.rolling(ave, win_type='triang').mean()
    df_country['ave'] = tmp.ave
    data = ColumnDataSource(df_country)

    tx = data.data['dateRep']
    if daily:
        ty = data.data['new']
        pic.line(tx, ty, legend_label=country+' daily new', color=color, line_dash='dashed')
        if ave > 0:
            ty=data.data['ave']
            pic.line(tx, ty, legend_label='%s %d-day rolling average' % (country, ave), color=color)
    else:
        ty = data.data['confirmed']
        pic.line(tx, ty, legend_label=country+' confirmed', color=color, line_dash='dashed')


def get_dataframe():
    url = 'https://interaktiv.morgenpost.de/data/corona/history.light.v4.csv'
    df = pd.read_csv(url)
    return df

def main(args):
    if args.html:
        output_file(args.html)
    colors = color_gen()
    df = get_dataframe()
    last_date = df['date'].max()
    title = '{}-{}'.format('-'.join(args.countries).upper(), last_date)
    p = figure(title=title, width=args.width, height=args.height)
    p.xaxis.formatter=DatetimeTickFormatter(days='%m/%d', months='%m/%d', years='%y%m%d')
    for country in args.countries:
        plot_a_country(p , df, country, args.daily, args.ave, args.per100k, next(colors))
    if args.png:
        export_png(p, filename=args.png)
    if args.html and args.show:
        show(p)


if __name__ == '__main__':
    argparser = ArgumentParser('python3 cli-corona.py', description="Cli Corona diagram generator")
    argparser.add_argument('countries', metavar='countries', type=str, nargs='+',
                           help="countries ISO 3166-1 alpha-2 code to track in the diagram")
    argparser.add_argument('--daily', action='store_true', dest='daily',
                           help="if set, include daily new cases, otherwise include cumulative number of cases")
    argparser.add_argument('--ave', dest='ave', type=int, default=7,
                           help="include AVE day rolling average. Effective only when --daily is set. Default=7")
    argparser.add_argument('--per100k', action='store_true', dest='per100k',
                           help="normalize the numbers to 100k population")
    argparser.add_argument('--width', dest='width', default=1000,
                           help="width of the diagram")
    argparser.add_argument('--height', dest='height', default=500,
                           help="height of the diagram")
    argparser.add_argument('--png', dest='png',
                           help="if set, diagram in png will be saved under this name")
    argparser.add_argument('--html', dest='html',
                           help="if set, html output will be saved under this name")
    argparser.add_argument('--show', action='store_true', dest='show',
                           help="if set, diagram will be shown in the browser. Only effective when --html is set")
    args = argparser.parse_args()
    main(args)


