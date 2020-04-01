import boto3
import numpy as np
from operator import itemgetter

from secrets import Secret

import requests
import pandas as pd
from flask import Flask
import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

s = Secret()

client = boto3.resource('dynamodb',
                        aws_access_key_id=s.aws_access_key_id,
                        aws_secret_access_key=s.aws_secret_access_key,
                        region_name='us-east-1')

table = client.Table('hahm-mood-dev')
items = table.scan()['Items']
person_data = {}

for moodlog in items:
    if moodlog['userId'] not in person_data:
        person_data[moodlog['userId']] = [ (  moodlog['createdAt'],moodlog['dayvalue'] ) ]
    else:
        person_data[moodlog['userId']].append((  moodlog['createdAt'],moodlog['dayvalue'] ))


avg_last_7 = {}

for person,mood_list in person_data.items():
    sorted_mood_list = sorted(mood_list,key=itemgetter(0), reverse=True)
    avg = 0
    count = 0
    while count < 7:
        avg += int(sorted_mood_list[count][1])
        count+=1
    avg = avg/7

    avg_last_7[person] = avg
##################################################################################################

def make_card(name,avg):
    return dbc.Card([
        dbc.CardBody(
            [
                html.H4(name, className="card-title"),
                daq.Gauge(
                    id=name+'_gauge',
                    label="Mood in past week",
                    value=avg,
                    max=10,
                    min=0,
                    showCurrentValue=True,
                    color={"gradient":True,"ranges":{"red":[0,4],"yellow":[4,7],"green":[7,10]}}
                ),
                dbc.Button("Details", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)




def make_card_layout():
    res = []
    names = list(avg_last_7.keys())
    avgs = list(avg_last_7.values())

    count = 0

    for i in range(len(names)):
        row = []
        for j in range(3):
            try:
                row.append(dbc.Col(html.Div(make_card(names[count], avgs[count])), md=4 ))
            except:
                pass
            count +=1

        if len(row) > 0:
            res.append(dbc.Row(row, style={"height": "45vh"},))

    return res

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.PULSE],
                assets_folder='assets')



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



divs = make_card_layout()


index_page = html.Div([
    html.Div([
        html.Div([
            html.H2('Therapist Dashboard Portal', className='display-4'),
            html.P('Here is where a medical professional would  get an overview of his/her patients', className='lead'),
            html.Hr(className="my-4"),
            html.P('The professional can click on a patient for more details and to contact directly'),
            html.A('Github', target="_blank",className='btn btn-primary btn-lg', href="https://github.com/jagath-jaikumar/HAHM",role="button")
        ],
        className='container text-center'
        )
        ],className='jumbotron')





    ,
    html.Div(divs, className='container')
])

test_page = html.Div([
    html.H1('test')
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/test':
        return test_page
    else:
        return index_page


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True, host='0.0.0.0')
