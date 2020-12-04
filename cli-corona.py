# MIT License
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
from argparse import ArgumentParser, ArgumentTypeError

def color_gen():
    yield from itertools.cycle(Category10[10])

def plot_a_id(pic, df, id, daily, ave, cumu, per100k, color, col):
    df_country=df[df['id'] == id]
    df_country['dateRep'] = pd.to_datetime(df.date, format='%Y%m%d')

    tmp = df_country[[col]]
    df_country['new'] = tmp.diff(periods=1,axis=0)
    if (per100k):
        df_country['new'] = df_country['new'] / df_country['population'] * 100000
    if ave > 0:
        df_country['ave'] = df_country['new'].rolling(ave).mean()
    data = ColumnDataSource(df_country)

    tx = data.data['dateRep']
    if daily:
        ty = data.data['new']
        daily_line_dash = 'dashed' if ave > 0 else 'solid'
        pic.line(tx, ty, legend_label=id+' daily new', color=color, line_dash=daily_line_dash)
    if ave > 0:
        ty=data.data['ave']
        pic.line(tx, ty, legend_label='%s %d-day rolling average' % (id, ave), color=color)
    if cumu:
        ty = data.data[col]
        pic.line(tx, ty, legend_label='%s' % (id), color=color, line_dash='dotted')


def get_dataframe(start, end):
    url = 'https://interaktiv.morgenpost.de/data/corona/history.light.v4.csv'
    df = pd.read_csv(url)
    if start:
        df = df[df['date'] >= start]
    if end:
        df = df[df['date'] <= end]
    return df


def search(df, search_item):
    res = df[['id', 'label', 'label_en']][
                                         df['label'].str.contains(search_item, case=False)
                                         | df['label_en'].str.contains(search_item, case=False)
    ].drop_duplicates()
    for idx, row in res.iterrows():
        print('{}\t{}\t{}'.format(row['id'], row['label'], row['label_en']))

def main(args):
    df = get_dataframe(args.start, args.end)
    if args.search and len(args.search) > 0:
        print('id\tlabel\tlabel_en')
        for search_item in args.search:
            search(df, search_item.strip(','))
        return
    if args.html:
        output_file(args.html)
    colors = color_gen()
    first_date, last_date = df['date'].min(), df['date'].max()
    title = '{}-{}-{} {}'.format('-'.join(args.ids).upper(), first_date, last_date, args.col)
    if args.per100k: title = title + ' Per 100000'
    p = figure(title=title, width=args.width, height=args.height)
    p.xaxis.formatter=DatetimeTickFormatter(days='%m/%d', months='%m/%d', years='%y%m%d')
    for id in args.ids:
        plot_a_id(pic=p,
                       df=df,
                       id=id,
                       daily=args.daily,
                       ave=args.ave,
                       cumu=args.cumu,
                       per100k=args.per100k,
                       color=next(colors),
                       col=args.col,
                       )
    p.legend.location='top_left'
    if args.png:
        export_png(p, filename=args.png)
    if args.html and args.show:
        show(p)

def check_col(col):
    if col not in {'confirmed', 'recovered', 'deaths'}:
        raise ArgumentTypeError('must be one of "confirmed", "recovered", or "deaths"')
    return col

if __name__ == '__main__':
    argparser = ArgumentParser('python3 cli-corona.py', description="Cli Corona diagram generator")
    argparser.add_argument('--ids', type=str, nargs='*',
                           help="ids of regions to track in the diagram. Country ids are ISO 3166-1 alpha-2 codes. See also --search")
    argparser.add_argument('--search', type=str, nargs='*',
                           help="search for id")
    argparser.add_argument('--col', type=check_col, dest='col', default='confirmed',
                           help='one of "confirmed", "recovered", or "deaths"')
    argparser.add_argument('--daily', action='store_true', dest='daily',
                           help="if set, include daily new cases, otherwise include cumulative number of cases")
    argparser.add_argument('--ave', dest='ave', type=int, default=0,
                           help="include AVE day rolling average")
    argparser.add_argument('--cumu', action='store_true',
                           help="if set, include cumulative numbers")
    argparser.add_argument('--per100k', action='store_true', dest='per100k',
                           help="normalize the numbers to 100k population")
    argparser.add_argument('--width', dest='width', type=int, default=1000,
                           help="width of the diagram")
    argparser.add_argument('--height', dest='height', type=int, default=500,
                           help="height of the diagram")
    argparser.add_argument('--start', dest='start', type=int, help="first day to track. Format: yyyymmdd")
    argparser.add_argument('--end', dest='end', type=int, help="last day to track. Format: yyyymmdd")
    argparser.add_argument('--png', dest='png',
                           help="if set, diagram in png will be saved under this name")
    argparser.add_argument('--html', dest='html',
                           help="if set, html output will be saved under this name")
    argparser.add_argument('--show', action='store_true', dest='show',
                           help="if set, diagram will be shown in the browser. Only effective when --html is set")
    args = argparser.parse_args()
    main(args)


