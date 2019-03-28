import json
import requests 
from process import getIdAndType, getSubInfo, toJson, saveJson
from typing import Callable, Dict, Any
from util import compose

def crawlerMainJob(*params) -> Callable:
    return compose(
        lambda data : saveJson('./result.json', data),
        lambda data : getSubInfo(data, 650),
        getIdAndType,
        toJson,
        requests.get,
    )(*params)

def crawler(event : Dict, context : Any) -> None:
    itemURL = 'https://apis.zigbang.com/v3/items2'
    itemURLPayload = {}
    if event['test']:
        # loads only ~ 50 items
        itemURLPayload = {
            'lat_south': 37.3553425382805,
            'lat_north': 37.411170336344824,
            'lng_west': 126.76330145291172,
            'lng_east': 126.88466634965496,
            'room': '[01,02,03,04,05]'
        }
    else:
        # loads ~30000 items
        itemURLPayload = {'lat_south': 37.44033750792432, 'lat_north': 37.6917904425295, 'lng_west': 126.87271708120215, 'lng_east': 127.08344785550588, 'room': '[01,02,03,04,05]'}
    
    crawlerMainJob(itemURL, itemURLPayload)
    
if __name__ == "__main__":
    crawler({'test': True},1)