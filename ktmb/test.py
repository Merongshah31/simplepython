import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import html, dcc
import datetime
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Interval(
        id='interval-map',
        interval=25 * 1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='map-container'),  # Container for the map
    html.H1("KTMB"),
    html.Div(id='live-update-text'),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # in milliseconds
        n_intervals=0
    )
])

def get_ktmdata():
    # Sample GTFS-R URL from Malaysia's Open API
    URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/ktmb'
    # Parse the GTFS Realtime feed
    feed = gtfs_realtime_pb2.FeedMessage()
    response = get(URL)
    feed.ParseFromString(response.content)

    # Extract and print vehicle position information
    vehicle_positions = []
    for entity in feed.entity:
        vehicle_dict = MessageToDict(entity)
        if 'vehicle' in vehicle_dict and 'position' in vehicle_dict['vehicle']:
            vehicle_positions.append({
                'timestamp': vehicle_dict.get('timestamp', None),
                'trip_id': vehicle_dict['vehicle']['trip'].get('trip_id', None),
                'latitude': vehicle_dict['vehicle']['position'].get('latitude', None),
                'longitude': vehicle_dict['vehicle']['position'].get('longitude', None),
                'bearing': vehicle_dict['vehicle']['position'].get('bearing', None),
                'speed': vehicle_dict['vehicle']['position'].get('speed', None),
                'vehicle_id': vehicle_dict['vehicle']['vehicle'].get('id', None),
                'vehicle_label': vehicle_dict['vehicle']['vehicle'].get('label', None)
            })

    print(f'Total vehicles: {len(vehicle_positions)}')
    df = pd.DataFrame(vehicle_positions)
    #print(df)
    
    return df

@app.callback(
    Output('live-update-text', 'children',),
    Input('interval-component', 'n_intervals')
)
def update_time(n):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Current Time: {current_time}"

@app.callback(
    Output('map-container', 'children'),
    Input('interval-map', 'n_intervals')
)
def update_map(n_intervals):
    print("Updating map..")
    df = get_ktmdata()
    if len(df) == 0:
        return "No data available"

    markers = [
        dl.Marker(
            position=[row['latitude'], row['longitude']],
            children=[
                dl.Tooltip(f"vehicle_label: {row['vehicle_label']}")
            ],
            id={'type': 'marker', 'index': i},  # Unique id for each marker
            n_clicks=0,  # Initialize number of clicks on each marker
        )
        for i, row in df.iterrows()
    ]
    
    # Center the map on the first vehicle
    center = (df.iloc[0]['latitude'], df.iloc[0]['longitude'])

    # Create a list of vehicle labels
    vehicle_labels = [html.Li(row['vehicle_label']) for i, row in df.iterrows()]

    return dbc.Row([
        dbc.Col([
            dl.Map(
                children=[
                    dl.TileLayer(),
                    *markers,
                ],
                center=center,
                zoom=11,
                style={'height': '85vh'},
                id='map',
            ),
        ], width=10),  #bootstrap 
        dbc.Col([
            dbc.ListGroup(vehicle_labels, flush=True)
        ], width=2)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
