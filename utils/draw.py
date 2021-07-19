import plotly.graph_objects as go
from base64 import b64encode
import dash_html_components as html
import dash_core_components as dcc
from plotly.subplots import make_subplots
import pandas as pd

def fig2img(fig):
    img_bytes = fig.to_image(format="png")
    encoding = b64encode(img_bytes).decode()
    img_b64 = "data:image/png;base64," + encoding
    return html.Img(src=img_b64, style={'width': '100%'})

def fig2dcc(fig):
    return dcc.Graph(figure=fig)

def plot_price(df, flag):
    dt_all = pd.date_range(start=df.index.to_series().iloc[0],end=df.index.to_series().iloc[-1])
    dt_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in pd.to_datetime(df.index.to_series(), format="%Y-%m-%d %H:%M:%S")]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in dt_obs]

    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, vertical_spacing=0.03, row_width = [0.2,0.7])
    fig.update_layout(autosize=False, width=1000, height=1000)
    fig.update_xaxes(rangebreaks=[dict(values = dt_breaks)])
    fig.add_trace(go.Candlestick(x = df.index.to_series(), open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],showlegend=False),row=1, col=1)
    fig.add_trace(go.Bar(x = df.index.to_series(), y=df['Volume'],showlegend=False),row=2, col=1)
    fig.update(layout_xaxis_rangeslider_visible=False)
    # layout = go.Layout(xaxis=dict(type='category'), autosize=False, width=1000, height=1000)
    # fig = go.Figure(data=[go.Candlestick(x=df.index.to_series(),open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'])],
    #                 layout=layout)
    if flag == 'img':
        return fig2img(fig)
    else:
        return fig2dcc(fig)

def plot_price_ind(df, flag, indicator = "sma"):
    dt_all = pd.date_range(start=df.index.to_series().iloc[0],end=df.index.to_series().iloc[-1])
    dt_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in pd.to_datetime(df.index.to_series(), format="%Y-%m-%d %H:%M:%S")]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in dt_obs]


    # use pandas ta here to draw indicator
    
    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, vertical_spacing=0.03, row_width = [0.2,0.7])
    fig.update_layout(autosize=False, width=1000, height=1000)
    fig.update_xaxes(rangebreaks=[dict(values = dt_breaks)])
    fig.add_trace(go.Candlestick(x = df.index.to_series(), open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],showlegend=False),row=1, col=1)
    fig.add_trace(dfsma,row=1, col=1)
    fig.add_trace(go.Bar(x = df.index.to_series(), y=df['Volume'],showlegend=False),row=2, col=1)
    fig.update(layout_xaxis_rangeslider_visible=False)
    # layout = go.Layout(xaxis=dict(type='category'), autosize=False, width=1000, height=1000)
    # fig = go.Figure(data=[go.Candlestick(x=df.index.to_series(),open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'])],
    #                 layout=layout)
    if flag == 'img':
        return fig2img(fig)
    else:
        return fig2dcc(fig)
