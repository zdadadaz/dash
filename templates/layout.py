import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from utils.dash_utils import make_table, make_table_hold, make_card, ticker_inputs, make_item


available_intervals = ['30m', 'day','week','month']

def layout_dash(df, dropid='interval-dropdown', radid='period-radio', graphid = 'ytd-graph',tableid='table-hold-all'):
    return dbc.Row([
                dbc.Row([
                     drop_radio_graph(dropid=dropid, radid=radid, graphid = graphid)
                ]),
                dbc.Col( make_table_hold(tableid,df, '17px', 4 ))
            ])

def drop_radio_graph(dropid='interval-dropdown', radid='period-radio', graphid = 'ytd-graph'):
    return dbc.Col([
                        dcc.Dropdown(
                            id=dropid,
                            options=[{'label': i, 'value': i} for i in available_intervals],
                            value='day'
                        ),
                        dbc.Row(dcc.RadioItems(
                            id=radid,
                            options=[{'label': i, 'value': i} for i in ['ytd','1 year','2 year','5 year','10 year', 'all']],
                            value='ytd',
                            labelStyle={'display': 'inline-block'},
                        ),justify="end"),
                        dbc.Col(id=graphid, width={"size": 30, "order": "last"}) # "offset": 3
                    ])

def create_layout():
    return html.Div([
        dbc.Row([dbc.Col([make_card("Enter Ticker", "success", 
        [html.H1(
            children='Hello Dash',
            style={
                'textAlign': 'center'
            }
        )],
        ), 
            html.Div([
                dcc.Location(id='url',refresh=False),
                dcc.Link('Go to Holdlist', href='/dash/'),
                html.Br(),
                dcc.Link('Go to Watchlist', href='/apps/app1'),
                html.Br(),
                dcc.Link('Go to screener', href='/apps/app2'),
                html.Br()])
            ])]),
            dbc.Row([html.Div(id='page-content')])
        ])


