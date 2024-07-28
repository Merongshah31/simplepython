import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, dcc
import datetime
from dash.dependencies import Input, Output

from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

app = Dash(__name__)

app.layout = html.Div([
    dcc.Interval(
        id='interval-map',
        interval=25*1000,  # in milliseconds
        n_intervals=0
    ),
    dl.Map([
        dl.TileLayer(),
        dl.GeoJSON(data=dlx.dicts_to_geojson([dict(lat=0, lon=0)]), cluster=True),
        dl.GeoJSON(url='/assets/markers_1k.json', cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100}),
    ],
           center=(0, 0),
           zoom=11,
           style={'height': '85vh'}, 
           id='map'),
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
                'vehicle_id': vehicle_dict['vehicle'],
                'vehicle_label': vehicle_dict['vehicle'].get('label', None)
            })

    print(f'Total vehicles: {len(vehicle_positions)}')
    df = pd.DataFrame(vehicle_positions)
    
    return df

@app.callback(
    Output('live-update-text', 'children',),
    Input('interval-component', 'n_intervals')
)
def update_time(n):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Current Time: {current_time}"

@app.callback(
    Output('map', 'children'),
    Input('interval-map', 'n_intervals')
)
def update_map(n_intervals):
    LAT1, LON1, LAT2, LON2 = 0, 0, 0, 0  # Initialize to 0
    df = get_ktmdata()
    
    
    
    if not df.empty:
        if len(df) >= 2:  # Ensure at least two points are available
            row1 = df.iloc[0]
            LAT1 = float(row1['latitude'])
            LON1 = float(row1['longitude'])
            row2 = df.iloc[1]
            LAT2 = float(row2['latitude'])
            LON2 = float(row2['longitude'])
            #print("xxxx")
            print(LAT1, LON1, LAT2, LON2)
            #print(df)
            
            
        markers = [
            dl.Marker(
                position=[row['latitude'], row['longitude']],
                children=[
                    dl.Tooltip(f"Vehicle ID: {row['vehicle_id']['vehicle']}")
            ]
        )
        for i, row in df.iterrows()
    ]

    
    
    # Create a list of HTML list items containing vehicle information
    vehicle_list = []
    
    for i, row in df.iterrows():
        vehicle_list.append(html.Li(f"Vehicle ID: {row['vehicle_id']} - Latitude: {row['latitude']} - Longitude: {row['longitude']}"))
 
    return [
        dl.Map([
            dl.TileLayer(),
            dl.GeoJSON(data=dlx.dicts_to_geojson([
                dict(lat=LAT1, lon=LON1),
                dict(lat=LAT2, lon=LON2)
            ]), cluster=True),
            dl.GeoJSON(url='/assets/markers_1k.json', cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100}),
        ], 
        #center=((LAT1 + LAT2) / 2, (LON1 + LON2) / 2),  # Center map between two points
        center=(LAT1,LON1) ,  # Center map between two points
        zoom=11,
        style={'height': '85vh'}, 
        id='map'),
        html.Div([
            html.H2("Vehicle Information"),
            html.Ul([
                html.Li(f"Vehicle ID: {row['vehicle_id']['vehicle']}")
                for i, row in df.iterrows()
            ])
        ])

    ]

if __name__ == '__main__':
    app.run_server(debug=True)