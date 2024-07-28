from google.transit import gtfs_realtime_pb2
import requests
from protobuf_to_dict import protobuf_to_dict

def get_ktmb_data():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('https://api.data.gov.my/gtfs-static/ktmb')
    #feed.ParseFromString(response.content)
    #print(response)     #200

    ktmb_dict = protobuf_to_dict(feed)
    return ktmb_dict

if __name__ == '__main__':
    ktmb_data = get_ktmb_data()
    #print(ktmb_data)
