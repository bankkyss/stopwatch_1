# from asyncio.proactor_events import _ProactorBaseWritePipeTransport
# from turtle import st
# import dash
# from dash import html,dcc
# from dash.dependencies import Output, Input, State
# from dash.exceptions import PreventUpdate
# import dash_bootstrap_components as dbc
# import datetime
# import time
# green_button_style = {'background-color': 'green',
#                       'color': 'white',
#                       'height': '50px',
#                       'width': '200px'}

# red_button_style = {'background-color': 'red',
#                     'color': 'white',
#                     'height': '50px',
#                     'width': '200px'}

# app = dash.Dash(name=__name__)

# app.layout = dbc.Container([
#                             dbc.Row([
#                                 dbc.Col(html.H2('', id='client-time'), width=10)
#                                     ]),
#                             dbc.Row([
#                                 dbc.Col(html.Button(children='lap', id='lap_button', style=green_button_style)),
#                                 dbc.Col(html.Button(children="Start", id="start_button", n_clicks=0, style=green_button_style)),
#                                     ]),
#                             dbc.Row([
#                                 dbc.Col(html.Table(id='datarow'))
#                             ]),
#                             dcc.Interval(id='interval', interval=600, n_intervals=0),
#                             dcc.Store(id='starttime',data=[]),
#                             dcc.Store(id='dommy',data={'dataf':'0'}),
#                             dcc.Store(id='timelap'),
#                             ])
    
# app.clientside_callback(
#     dash.dependencies.ClientsideFunction(
#         namespace='clientside',
#         function_name='update_timer'
#     ),
#     dash.dependencies.Output('client-time', 'children'),
#     [dash.dependencies.Input('interval', 'n_intervals')])

# @app.callback([Output('datarow', 'children')],Input('dommy', 'data'))
# def updatetable(data):
#     data=data['dataf'].split(',')
#     row=[html.Tr([html.Th(col) for col in ['laps','time']]) ]
#     numberrow=len(data)
#     if numberrow-10<0:
#         numberrowf=0
#     else:
#         numberrowf=numberrow-10
#     for i in range(numberrow-1,numberrowf,-1):
#         row+=[html.Tr([html.Th(i),html.Th(data[i])])]
#     return([row])

# @app.callback(
#     [Output('start_button', 'children'),
#      Output('start_button', 'style'),
#      Output('starttime', 'data')],
#     [Input('start_button', 'n_clicks')]
#     )
# def update_button(n_clicks):
    
#     bool_disabled = n_clicks % 2
#     if bool_disabled:
#         print(datetime.datetime.timestamp(datetime.datetime.now()))
#         return "Stop ", red_button_style,datetime.datetime.timestamp(datetime.datetime.now())
#     else:
#         return "Start ", green_button_style,[]

# @app.callback([Output('dommy', 'data')],
#     [Input('lap_button', 'n_clicks')],
#     [State('dommy', 'data'),State('starttime', 'data')]
#     )
# def lapdata(n_clicks,data,start):
#     if n_clicks is None:
#         raise PreventUpdate
#     if start!=[]:
#         diff=datetime.datetime.timestamp(datetime.datetime.now())-start
#         print(diff)
#         data['dataf']=data['dataf']+','+'{:.3f}'.format(diff)
#     return([data])


# if __name__ == '__main__':
#     app.run_server(debug=True, port=8077, threaded=True)