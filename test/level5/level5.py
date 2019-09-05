import json
from datetime import datetime

output = []


# return number of days
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days) + 1


# return days cost
def days_cost(c, d):
    if d > 10:
        c = c - (c * (50 / 100))
        return d * c
    elif d > 4:
        c = c - (c * (30 / 100))
        return d * c
    elif d > 1:
        c = c - (c * (10 / 100))
        return d * c
    else:
        return d * c


# reading from file and saving data on data_
with open('input.json') as json_file:
    data = json.load(json_file)
    for i in data['cars']:
        for j in data['rentals']:
            if i['id'] == j['car_id']:
                price = (i['price_per_km'] * j['distance']) + days_cost(i['price_per_day'],
                                                                        days_between(j['start_date'], j['end_date']))
                commission = price * 30 / 100
                assistance_fee = days_between(j['start_date'], j['end_date']) * 100
                options = []
                for y in data['options']:
                    if j['id'] == y['rental_id']:
                        options += [y['type']]
                output += [{'id': j['id'],
                            'options': options,
                            'actions': [
                                {
                                    'who': 'driver',
                                    'type': 'debit',
                                    'amount': price,
                                },
                                {
                                    'who': 'owner',
                                    'type': 'credit',
                                    'amount': price * 70 / 100,
                                },
                                {
                                    'who': 'insurance',
                                    'type': 'credit',
                                    'amount': commission / 2,
                                },
                                {
                                    'who': 'assistance',
                                    'type': 'credit',
                                    'amount': assistance_fee,
                                },
                                {
                                    'who': 'drivy',
                                    'type': 'credit',
                                    'amount': commission - ((commission / 2) + assistance_fee),
                                }
                            ]
                            }]
                data_ = {"rentals": output}

# writing in new file
myfile = open('output.json', 'w')
myfile.writelines(json.dumps(data_))
myfile.close()
