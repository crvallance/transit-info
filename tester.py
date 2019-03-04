import secrets
import requests
from datetime import datetime, timedelta

class ScheduledEvent(object):
    def __init__(self):
        self.arrT = datetime
        self.name = ''
        self.trvlT = datetime
        self.timestamp = ''
        self.prdct = ''

        
def train_times():
    train_url = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?outputType=JSON&key='
    rockwell_id = '41010'
    rockwell_url = train_url + secrets.train_tracker + '&mapid={}'.format(rockwell_id)
    rockwell_walk = 14
    r_times = requests.get(rockwell_url)
    times_data = r_times.json() 
    all_times = []
    for eta in times_data['ctatt']['eta']:
        # print(eta.keys())
        if 'Loop' in eta['stpDe']:
            # print(eta['stpDe'])
            # print(eta['rn'])
            # print(eta['arrT'])
            arrT = datetime.strptime(eta['arrT'], '%Y-%m-%dT%H:%M:%S')
            travel_time = (arrT + timedelta(minutes=rockwell_walk))
            # print(arrT)
            time = ScheduledEvent()
            time.arrT = arrT
            time.name = eta['rn']
            time.trvlT = arrT + timedelta(minutes=rockwell_walk)
            all_times.append(time)
            # print('To make the {} train ({}), leave by {}'.format(eta['rn'], travel_time.strftime('%I:%M:%S'), arrT.strftime('%I:%M:%S')))
    return(all_times)

def bus_times():
    bus_route = '11'
    foster_western = '14965'
    bus_url = 'http://www.ctabustracker.com/bustime/api/v2/getpredictions?format=json&key={}&stpid={}&rd={}'.format(secrets.bus_tacker, foster_western, bus_route)
    r_times = requests.get(bus_url)
    times_data = r_times.json()
    all_times = []
    # print(times_data)
    if 'error' in times_data['bustime-response']:
        print('Bus error: {}'.format(times_data['bustime-response']['error'][0]['msg']))
    else:
        for bus in times_data['bustime-response']:
            arrT = datetime.strptime(bus['prdtm'], '%Y-%m-%d %H:%M')
            time = ScheduledEvent()
            time.arrT = arrT
            time.name = bus['vid']
            time.prdct = bus['prdctdn']
            all_times.append(time)
            # print('The {} bus ({}) will be here in {} minutes'.format(bus['vid'], arrT.strftime('%I:%M'), bus['prdctdn']))
    return(all_times)

def main():
    trains = train_times()
    for train in trains:
        print('To make the {} train ({}), leave by {}'.format(train.name, train.trvlT.strftime('%I:%M:%S'), train.arrT.strftime('%I:%M:%S')))
    busses = bus_times()
    for bus in busses:
        print('The {} bus ({}) will be here in {} minutes'.format(bus.name, bus.arrT.strftime('%I:%M'), bus.prdct))

if __name__ == "__main__":
    # execute only if run as a script
    # train_times()
    # bus_times()
    main()

