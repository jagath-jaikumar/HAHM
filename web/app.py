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
import plotly.express as px

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
    link = '/'+name
    return dbc.Card([
        dbc.CardBody(
            [
                html.Div([
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
                    dbc.Button("Details",href=link, color="primary"),
                ],className="container text-center")

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
                row.append(dbc.Col(html.Div(make_card(names[count], avgs[count])),style={"width": "auto", "padding":"10px"}, md=4,width=3 ))
            except:
                pass
            count +=1

        if len(row) > 0:
            res.append(dbc.Row(row, style={"height": "auto", "padding":"10px"},))

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




def makeUserCharts(name):
    result = []
    mood_list = person_data[name]
    sorted_mood_list = sorted(mood_list,key=itemgetter(0), reverse=False)
    sorted_mood_list_rev = sorted(mood_list,key=itemgetter(0), reverse=True)

    moodHistory = []
    for date, mood in sorted_mood_list:
        moodHistory.append(int(mood))

    last = 7


    last7UserUpdate = sorted_mood_list_rev[0:last]
    last7UserUpdate.reverse()
    lastUserUpdate = last7UserUpdate[-1]
    print(last7UserUpdate)
    last7UserUpdate = [int(x[1]) for x in last7UserUpdate]



    averageMoodHistory = np.mean(moodHistory)
    averageMoodLast7 = np.mean(last7UserUpdate)

#    print(lastUserUpdate)
#    print(last7UserUpdate)
#    print(averageMoodHistory)
#    print(averageMoodLast7)
    row1 = []
    row1.append(
        dbc.Col(
            dbc.Card([
                dbc.CardBody(
                    [
                        html.Div([
                            html.H4('Last Recorded Mood', className="card-title"),
                            daq.Gauge(
                                id=name+'_gauge',
                            #    label="Last Recorded Mood",
                                value=int(lastUserUpdate[1]),
                                max=10,
                                min=0,
                                showCurrentValue=True,
                                color={"gradient":True,"ranges":{"red":[0,4],"yellow":[4,7],"green":[7,10]}}
                            ),
                        ],className="container text-center")

                    ]
                ),
            ],
            style={"width": "22rem"},
            ),width=4
        )
    )

    row1.append(
        dbc.Col(
            dbc.Card([
                dbc.CardBody(
                    [
                        html.Div([
                            html.H4('Average Mood Last 7 Days', className="card-title"),
                            daq.Gauge(
                                id=name+'_gauge',
                            #    label="Average Mood Last 7 Days",
                                value=averageMoodLast7,
                                max=10,
                                min=0,
                                showCurrentValue=True,
                                color={"gradient":True,"ranges":{"red":[0,4],"yellow":[4,7],"green":[7,10]}}
                            ),
                        ],className="container text-center")

                    ]
                ),
            ],
            style={"width": "22rem"},
            ),width=4
        )
    )

    row1.append(
        dbc.Col(
            dbc.Card([
                dbc.CardBody(
                    [
                        html.Div([
                            html.H4('Average Mood All Time', className="card-title"),
                            daq.Gauge(
                                id=name+'_gauge',
                            #    label="Average Mood Last 7 Days",
                                value=averageMoodHistory,
                                max=10,
                                min=0,
                                showCurrentValue=True,
                                color={"gradient":True,"ranges":{"red":[0,4],"yellow":[4,7],"green":[7,10]}}
                            ),
                        ],className="container text-center")

                    ]
                ),
            ],
            style={"width": "22rem"},
            ),width=4
        )
    )

    result.append(dbc.Row(row1, style={"height": "auto", "padding":"10px"},))

    fig = px.line(x=range(7,0,-1),
                  y=last7UserUpdate,
                  labels={'x':'Days Ago', 'y':'Day Value 0-10'},
                  )
    fig.update_layout(title='Moods recorded in past week',
                   xaxis_title='Days Ago',
                   yaxis_title='Mood Recording',
                   xaxis=dict(showticklabels=True,),
                   )
    fig.update_xaxes(autorange="reversed")
    result.append(dcc.Graph(figure=fig, id='graph'))




    return result




def indivUserPage(pathname):
    name = pathname[1:].split('%20')
    name = ' '.join(name)
    if name not in person_data:
        return html.Div([
            html.Div([
                html.H2('Error:  Name not found', className='display-4'),
                ],
            className='container text-center'
            )
            ],className='jumbotron')

    charts = makeUserCharts(name)


    layout = html.Div([
    html.Div([
        html.Div([
            html.H2(name, className='display-4'),
            html.P('Here is where a medical professional would  get a detailed view on this patient', className='lead'),
            html.Hr(className="my-4"),
            html.P('The following data is updated in real time'),
            html.A('Back to overview',className='btn btn-primary btn-lg', href="/",role="button")
        ],
        className='container text-center'
        )
        ],className='jumbotron'),

        html.Div(charts, className='container')
    ])

    return layout





# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '':
        return index_page

    return indivUserPage(pathname)


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True, host='0.0.0.0')
