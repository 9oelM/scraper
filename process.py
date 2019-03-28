import json
import requests 
from util import getNumbers 
from typing import Any, Dict, List

def getJson(file : str) -> Dict[str, Any]:
    with open(file) as f:
        data = json.load(f)
    return data

def toJson(response : Dict[str, Any]) -> List[int]:
    return response.json()

def saveJson(file : str, data : Dict[str, Any]) -> None:
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def getIdAndType(data : List) -> List:
    processed = []
    print('Total items requested: %d' %(len(data['list_items'])))
    for room in enumerate(data['list_items']):
        processed.append(
            { 'id': room[1]['simple_item']['item_id'], 
              'type': room[1]['section_type']
            }
        )
    return processed

def getSelectiveValues(itemDetail : List[any]) -> Dict[str, Any]:
    info = ['local2', 'local3', 'agent_lat', 'agent_lng', 'deposit', 'rent', 'manage_cost', 'floor', 'floor_all', 'building_type', 'near_subways', 'options', 'parking', 'room_type', 'size_m2', 'id', 'is_premium']
    room = {}
    for subinfo in info:
        if subinfo in ['manage_cost', 'floor', 'floor_all']:
            itemDetail[subinfo] = getNumbers(itemDetail[subinfo])
        room.update({
            subinfo: itemDetail[subinfo]
        })
    return room

def getSubInfo(data : List, step : int) -> Dict[str, Any]:
    detailedItemURL = 'https://apis.zigbang.com/v3/items'
    detailedItemURLPayload = {'detail':'true', 'item_ids': ''}
    # the number of data to be processed usually reaches up to ~30000 
    # divide the requests into each with 650 items
    
    result = []
    for counter, piece in enumerate(data):
        # step max < ~650
        if ( counter != 0 and counter % step == 0) or ( counter == len(data) -1):
            print('Reached %dth counter' %counter)
            print('Requesting')
            
            detailedItemURLPayload['item_ids'] = '[%s]' %detailedItemURLPayload['item_ids'][:-1]
            
            resp = requests.get(detailedItemURL, params=detailedItemURLPayload)
            
            print('Response received')
            
            for idx, item in enumerate(resp.json()['items']):
                itemDetail = item['item']
                room = getSelectiveValues(itemDetail)
                result.append(room)
                
            # reset
            detailedItemURLPayload['item_ids'] = ''
        else:
            detailedItemURLPayload['item_ids'] += '%d,' % piece['id']
            
    return {
        'length': len(result),
        'array': result
    }