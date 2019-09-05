import json
from datetime import datetime

output = []


# count days
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)+1


# reading from file and saving data on data_
with open('input.json') as json_file:
    data = json.load(json_file)
    for i in data['cars']:
        for j in data['rentals']:
            if i['id'] == j['car_id']:
                output += [{'id': j['id'],
                           'price': (i['price_per_km'] * j['distance']) + (i['price_per_day'] * days_between(j['start_date'], j['end_date']))}]
                data_ = {"rentals": output}

# writing in new file
myfile = open('output.json', 'w')
myfile.writelines(json.dumps(data_))
myfile.close()
