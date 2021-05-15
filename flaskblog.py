### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
from flask import Flask, render_template, url_for, flash, redirect
from forms import Addstock
from database.script import connect_sqlite
from templates.layout import create_layout, layout_dash
from utils.dash_utils import *
from utils.price_utils import get_today_price,get_year_price, Stocks
from datetime import date

server = Flask(__name__)
server.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app = dash.Dash(__name__,server = server ,\
                meta_tags=[{ "content": "width=device-width"}], \
                external_stylesheets=[dbc.themes.BOOTSTRAP],\
                url_base_pathname='/dash/')
app.config.suppress_callback_exceptions = True

cur_page = None
dbName = 'stock.db'

df = pd.read_csv('data/TW50.csv')
allStocks = Stocks([ str(i) for i in df['ticker']],'TW')
df = pd.DataFrame.from_dict(connect_sqlite(dbName, 'allhold'))
df = allStocks.output_dayprice_all(df)

dfw = pd.DataFrame.from_dict(connect_sqlite(dbName, 'allwatchlist'))
watchStocks = Stocks(dfw['ticker'],'TW')

today = date.today()
dfs = pd.read_csv('screener/{}.csv'.format(today))
screenStocks = Stocks([str(i) for i in dfs['ticker']],'TW')
page_watch = layout_dash(dfw, dropid='interval-dropdown-watch', radid='period-radio-watch', graphid = 'ytd-graph-watch',tableid='table-watch-all') 
page_hold = layout_dash(df, dropid='interval-dropdown', radid='period-radio', graphid = 'ytd-graph',tableid='table-hold-all') 
page_screen = layout_dash(dfs, dropid='interval-dropdown-screen', radid='period-radio-screen', graphid = 'ytd-graph-screen',tableid='table-screen-all') 
app.layout = create_layout()

@server.route("/")
@server.route("/home")
def home():
    stocks = connect_sqlite(dbName, 'allstock')
    a = ticker_inputs('ticker-input', 'date-picker', 36)
    return render_template('search.html', stocks=stocks)

# @server.route("/dash")
# def dash_home():
#     return app.index()

@server.route("/addhold", methods=['GET', 'POST'])
def addhold():
    form = Addstock()

    if form.validate_on_submit():
        conn = sqlite3.connect('stock.db')
        c = conn.cursor()
        
        #Add the new blog into the 'blogs' table
        query = 'insert into users VALUES (' + "'" + form.username.data + "',"  + "'" + form.email.data + "'," + "'" + form.password.data + "'" + ')' #Build the query
        c.execute(query) #Execute the query
        conn.commit() #Commit the changes

        flash(f'Add stock into hold success')
        return redirect(url_for('home'))
    return render_template('addhold.html', title='addhold', form=form)

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    cur_page = pathname
    if pathname == '/apps/app1':
        return page_watch
    elif pathname == '/apps/app2':
        return page_screen
    else:
        return page_hold

@app.callback(
    dash.dependencies.Output('ytd-graph-screen', 'children'),
    dash.dependencies.Input('table-screen-all', 'derived_virtual_data'),
    dash.dependencies.Input('table-screen-all', 'derived_virtual_selected_rows'),
    dash.dependencies.Input('interval-dropdown-screen', 'value'),
    dash.dependencies.Input('period-radio-screen', 'value'))
def update_graphs(rows, derived_virtual_selected_rows, interval, period):
    interval_dict={'30m':'30m' , 'day':'1d','week':'1wk', 'month':'1mo'}
    period_dict={'ytd':'ytd' ,'1 year':'1y','2 year':'2y','5 year':'5y','10 year':'10y', 'all':'max'}

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    rows = pd.DataFrame.to_dict(dfs) if rows is None else rows
    derived_virtual_selected_rows = 0 if len(derived_virtual_selected_rows)==0 else derived_virtual_selected_rows[0]
    # figs = allStocks.update_fig(interval=interval_dict[interval],period=period_dict[period])
    try:
        return screenStocks.update_one_fig(rows[derived_virtual_selected_rows]['ticker'], interval=interval_dict[interval],period=period_dict[period])
        # return figs[str(rows[derived_virtual_selected_rows]['ticker'])]
    except:
        print('prevent from initialization')

@app.callback(
    dash.dependencies.Output('ytd-graph-watch', 'children'),
    dash.dependencies.Input('table-watch-all', 'derived_virtual_data'),
    dash.dependencies.Input('table-watch-all', 'derived_virtual_selected_rows'),
    dash.dependencies.Input('interval-dropdown-watch', 'value'),
    dash.dependencies.Input('period-radio-watch', 'value'))
def update_graphs(rows, derived_virtual_selected_rows, interval, period):
    interval_dict={'30m':'30m' , 'day':'1d','week':'1wk', 'month':'1mo'}
    period_dict={'ytd':'ytd' ,'1 year':'1y','2 year':'2y','5 year':'5y','10 year':'10y', 'all':'max'}

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    rows = pd.DataFrame.to_dict(dfw) if rows is None else rows
    derived_virtual_selected_rows = 0 if len(derived_virtual_selected_rows)==0 else derived_virtual_selected_rows[0]
    # figs = allStocks.update_fig(interval=interval_dict[interval],period=period_dict[period])
    try:
        return watchStocks.update_one_fig(rows[derived_virtual_selected_rows]['ticker'], interval=interval_dict[interval],period=period_dict[period])
        # return figs[str(rows[derived_virtual_selected_rows]['ticker'])]
    except:
        print('prevent from initialization')


@app.callback(
    dash.dependencies.Output('ytd-graph', 'children'),
    dash.dependencies.Input('table-hold-all', 'derived_virtual_data'),
    dash.dependencies.Input('table-hold-all', 'derived_virtual_selected_rows'),
    dash.dependencies.Input('interval-dropdown', 'value'),
    dash.dependencies.Input('period-radio', 'value'))
def update_graphs(rows, derived_virtual_selected_rows, interval, period):
    interval_dict={'30m':'30m' , 'day':'1d','week':'1wk', 'month':'1mo'}
    period_dict={'ytd':'ytd' ,'1 year':'1y','2 year':'2y','5 year':'5y','10 year':'10y', 'all':'max'}

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    rows = pd.DataFrame.to_dict(df) if rows is None else rows
    derived_virtual_selected_rows = 0 if len(derived_virtual_selected_rows)==0 else derived_virtual_selected_rows[0]
    # figs = allStocks.update_fig(interval=interval_dict[interval],period=period_dict[period])
    try:
        return allStocks.update_one_fig(rows[derived_virtual_selected_rows]['ticker'], interval=interval_dict[interval],period=period_dict[period])
        # return figs[str(rows[derived_virtual_selected_rows]['ticker'])]
    except:
        print('prevent from initialization')
        

if __name__ == '__main__':
    app.run_server(debug=True)

