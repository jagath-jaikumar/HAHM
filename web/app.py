import boto3
import numpy as np
from operator import itemgetter

import requests
import pandas as pd
from flask import Flask
import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


client = boto3.resource('dynamodb',
                        aws_access_key_id='AKIA2CFFCDZLPX747O6A',
                        aws_secret_access_key='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',
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


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.PULSE],
                assets_folder='assets')



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



divs = []





index_page = html.Div([
    html.H1('index'),
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
