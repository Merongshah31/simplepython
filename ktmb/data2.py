from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

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
                'trip_id': vehicle_dict['vehicle']['trip'],
                'latitude': vehicle_dict['vehicle']['position'].get('latitude', None),
                'longitude': vehicle_dict['vehicle']['position'].get('longitude', None),
                'bearing': vehicle_dict['vehicle']['position'].get('bearing', None),
                'speed': vehicle_dict['vehicle']['position'].get('speed', None),
                'vehicle_id': vehicle_dict['vehicle'],
                'vehicle_label': vehicle_dict['vehicle'].get('label', None)
            })
            
    #data structure?
    
    #output        
    print(f'Total vehicles: {len(vehicle_positions)}')
    df = pd.DataFrame(vehicle_positions)
    row = df.iloc[0]
    print(row['latitude'], row['longitude'], row['trip_id'])
    row1 = df.iloc[1]
    print(row1['latitude'], row1['longitude'], row['trip_id'])
    #print(df[['latitude', 'longitude']])
    print(df)

    
    return df

if __name__ == '__main__':
    get_ktmdata()
