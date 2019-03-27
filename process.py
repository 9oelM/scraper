from __future__ import print_function # Python 2/3 compatibility
from decimal import Decimal
import boto3
import json
import requests 

def getJson(file):
    with open(file) as f:
        data = json.load(f)
    return data

def toJson(response):
    return response.json()

def getIdAndType(data):
    processed = []
    print('Total items requested: %d' %(len(data['list_items'])))
    for room in enumerate(data['list_items']):
        processed.append(
            { 'id': room[1]['simple_item']['item_id'], 
              'type': room[1]['section_type']
            }
        )
    return processed

def getSubInfo(data, step):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('houseData')
    
    detailedItemURL = 'https://apis.zigbang.com/v3/items'
    detailedItemURLPayload = {'detail':'true', 'item_ids': ''}
    # the number of data to be processed usually reaches up to ~30000 
    # divide the requests into each with 500 items
    
    for counter, piece in enumerate(data):
        result = []
        # step max < ~650
        if ( counter != 0 and counter % step == 0) or ( counter == len(data) -1):
            print('Reached %dth counter' %counter)
            print('Requesting')
            
            detailedItemURLPayload['item_ids'] = '[%s]' %detailedItemURLPayload['item_ids'][:-1]
            
            resp = requests.get(detailedItemURL, params=detailedItemURLPayload)
            
            print('Response received')
            
            for idx, item in enumerate(resp.json()['items']):
                itemDetail = item['item']
                info = ['agent_lat', 'agent_lng', 'deposit', 'rent', 'manage_cost', 'floor', 'floor_all', 'building_type', 'near_subways', 'options', 'parking', 'room_type', 'size_m2', 'id', 'is_premium']
                
                room = {}
                for subinfo in info:
                    room.update({
                        subinfo: itemDetail[subinfo]
                    })
                room = json.dumps(room)
                table.put_item(
                    Item=json.loads(room, parse_float = Decimal)
                )
                result.append(room)
                print(room)
                
            # reset
            detailedItemURLPayload['item_ids'] = ''
        else:
            detailedItemURLPayload['item_ids'] += '%d,' % piece['id']
            
    return result