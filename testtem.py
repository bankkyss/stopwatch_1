# from asyncio.proactor_events import _ProactorBaseWritePipeTransport
# from tracemalloc import start
# from turtle import st
from datetime import timedelta
import dash
from dash import html,dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import datetime
import pandas as pd
green_button_style = {'background-color': 'green',
                      'color': 'white',
                      'height': '50px',
                      'width': '200px'}

red_button_style = {'background-color': 'red',
                    'color': 'white',
                    'height': '50px',
                    'width': '200px'}

app = dash.Dash(name=__name__)

app.layout = dbc.Container([
                            dbc.Row([
                                dbc.Col(html.H2('', id='client-time'), width=10)
                                    ]),
                            dbc.Row([
                                dbc.Col(html.Button(children='lap', id='lap_button',n_clicks_timestamp=0, style=green_button_style)),
                                dbc.Col(html.Button(children='reset', id='reset_button',n_clicks_timestamp=0, style=red_button_style)),
                                dbc.Col(html.Button(children='stop', id='stop_button',n_clicks_timestamp=0, style=red_button_style)),
                                dbc.Col(html.Button(children="Start", id="start_button",n_clicks_timestamp=0,style=green_button_style)),
                                    ]),
                            dbc.Row([
                                dbc.Col(html.Table(id='datarow'))
                            ]),
                            dbc.Row(
                                [
                                html.Button("Download CSV", id="btn_csv"),
                                dcc.Download(id="download-dataframe-csv"),
                                ]
                            ),
                            dcc.Interval(id='interval', interval=200, n_intervals=0),
                            dcc.Store(id='starttime',data=[]),
                            dcc.Store(id='pastime',data={'time':0}),
                            dcc.Store(id='timelap',data={'dataf':'0'}),
                            dcc.Store(id='dommy'),
                            ])
    
app.clientside_callback(
    dash.dependencies.ClientsideFunction(
        namespace='clientside',
        function_name='difftime'
    ),
    Output('client-time', 'children'),
    [Input('interval', 'n_intervals'),Input('starttime','data'),Input('pastime','data')])


@app.callback([Output('starttime','data'),
            Output('start_button', 'style'),
            Output('stop_button', 'style'),
            Output('lap_button', 'style'),
            Output('reset_button', 'style'),],
            [Input('start_button','n_clicks_timestamp'),
            Input('stop_button','n_clicks_timestamp')],
            )
def starttime(timestart,timestop):
    st=green_button_style
    sp=red_button_style
    lp=green_button_style
    rs=red_button_style
    if int(timestart)>int(timestop):
        start=datetime.datetime.timestamp(datetime.datetime.now())
        st=dict(display='none')
        rs=dict(display='none')
    elif int(timestart)<int(timestop):
        sp=dict(display='none')
        lp=dict(display='none')
        start=[]
    else :
        start=[]
        sp=dict(display='none')
        rs=dict(display='none')
    return start,st,sp,lp,rs


@app.callback([Output('timelap','data')],
            [Input('lap_button','n_clicks_timestamp'),Input('reset_button','n_clicks_timestamp')],
            [State('timelap', 'data'),State('starttime', 'data'),State('pastime','data')]
    )
def lapdata(laptime,resettime,data,start,pastime):
    if laptime is None:
        raise PreventUpdate
    if int(laptime)>int(resettime):
        if start!=[]:
            diff=datetime.datetime.timestamp(datetime.datetime.now())-start
            #print(diff)
            data['dataf']=data['dataf']+','+'{:.3f}'.format(diff+pastime['time'])
            #print(data)
    else:
        data['dataf']='0'
    return([data])

@app.callback([Output('datarow', 'children')],Input('timelap', 'data'))
def updatetable(data):
    data=data['dataf'].split(',')
    row=[html.Tr([html.Th(col) for col in ['laps','time']]) ]
    numberrow=len(data)
    if numberrow-10<0:
        numberrowf=0
    else:
        numberrowf=numberrow-10
    for i in range(numberrow-1,numberrowf,-1):
        row+=[html.Tr([html.Th(i),html.Th(str(timedelta(seconds=float(data[i])))[:11])])]
    return([row])

@app.callback([Output('pastime','data')],
            [Input('stop_button','n_clicks_timestamp'),Input('reset_button','n_clicks_timestamp')],
            [State('pastime', 'data'),State('starttime', 'data')]
    )
def pastime(stoptime,resettime,pasdata,start):
    if int(stoptime)>int(resettime):
        diff=datetime.datetime.timestamp(datetime.datetime.now())-start
        pasdata['time']=pasdata['time']+diff
    else:
        pasdata['time']=0
    return[pasdata]


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('timelap', 'data'),
    prevent_initial_call=True,
)
def loaddata(n_clicks,data):
    data=[str(timedelta(seconds=float(i)))[:11] for i in data['dataf'].split(',')[1:]]
    df=pd.DataFrame({'lap':[i+1 for i in range(len(data))],'time(sec)':data}).set_index('lap')
    return dcc.send_data_frame(df.to_csv, "mydf.csv")

@app.callback(Output('btn_csv','style'),[Input('stop_button','n_clicks_timestamp'),Input('start_button','n_clicks_timestamp'),Input('reset_button','n_clicks_timestamp')])
def showload(starttime,stoptime,resettime):
    #print(starttime,stoptime,resettime)
    if starttime<=stoptime :
        return dict(display='none')
    elif resettime>=stoptime:
        return dict(display='none')
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True, port=8077, threaded=True)