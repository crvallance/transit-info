import secrets
import requests
from datetime import datetime, timedelta

class ScheduledEvent(object):
    def __init__(self):
        self.arrT = arrT
        self.name = name
        self.ccopass = ccopass
        self.trvlT = trvlT
        self.timestamp = timestamp
        
        
def train_times():
    train_url = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?outputType=JSON&key='
    rockwell_id = '41010'
    rockwell_url = train_url + secrets.train_tracker + '&mapid={}'.format(rockwell_id)
    rockwell_walk = 14
    r_times = requests.get(rockwell_url)
    times_data = r_times.json() 
    for eta in times_data['ctatt']['eta']:
        # print(eta.keys())
        if 'Loop' in eta['stpDe']:
            # print(eta['stpDe'])
            # print(eta['rn'])
            # print(eta['arrT'])
            arrT = datetime.strptime(eta['arrT'], '%Y-%m-%dT%H:%M:%S')
            travel_time = (arrT + timedelta(minutes=rockwell_walk))
            # print(arrT)
            print('To make the {} train ({}), leave by {}'.format(eta['rn'], travel_time.strftime('%I:%M:%S'), arrT.strftime('%I:%M:%S')))

def bus_times():
    bus_route = '11'
    foster_western = '14965'
    bus_url = 'http://www.ctabustracker.com/bustime/api/v2/getpredictions?format=json&key={}&stpid={}&rd={}'.format(secrets.bus_tacker, foster_western, bus_route)
    r_times = requests.get(bus_url)
    times_data = r_times.json()
    # print(times_data)
    if 'error' in times_data['bustime-response']:
        print('Bus error: {}'.format(times_data['bustime-response']['error'][0]['msg']))
    else:
        for bus in times_data['bustime-response']:
            arrT = datetime.strptime(bus['prdtm'], '%Y-%m-%d %H:%M')
            print('The {} bus ({}) will be here in {} minutes'.format(bus['vid'], arrT.strftime('%I:%M'), bus['prdctdn']))

if __name__ == "__main__":
    # execute only if run as a script
    train_times()
    bus_times()

