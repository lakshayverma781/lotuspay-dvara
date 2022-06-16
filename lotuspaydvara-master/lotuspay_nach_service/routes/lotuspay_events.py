from fastapi import APIRouter, Depends, status, Body, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import json
import requests
from typing import Dict
from Crypto.Cipher import AES
from base64 import b64decode
from databases import Database
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.resource.generics import response_to_dict
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs


from lotuspay_nach_service.data.events_model import (
events
)


router = APIRouter()

LOTUSPAY_SERVER = 'lotus-pay-server'


@router.post("/lotuspay-events",  status_code=status.HTTP_200_OK,  tags=["Lotuspay Events"])
async def create_events(
    payload: Dict = Body(...),
    # payload: Request,
    database: Database = Depends(get_database)
):
    try:
        msg = payload['serialized_response']
        test = json.dumps(msg)
        print('printing serialized response - ', test)
        iv = msg[:16].encode('utf-8')
        decipher = AES.new('whk_:PqnYy_VUz7Z'.encode('utf-8'), AES.MODE_CBC, iv=iv)
        cipher_text = b64decode(msg[16:].encode('utf-8'))
        data = decipher.decrypt(cipher_text)
        print('printing data - ', data)
        splitted = data.split(b'\x03')[0]
        dict_str = splitted.decode("utf-8")
        data_dict = json.loads(dict_str)
        print('response dictionary - ', data_dict)
        store_events = {}
        store_events['event_id']=data_dict.get('id')
        store_events['event_object'] = data_dict.get('object')
        store_events['event_created'] = data_dict.get('created')
        store_events['event_livemode'] = data_dict.get('livemode')
        store_data = data_dict.get('data')
        store_events['resource_id'] = store_data.get('id')
        store_events['resource_object'] = store_data.get('object')
        store_events['resource_created'] = store_data.get('created')
        store_events['resource_status'] = data_dict.get('type')
        store_events['created_date'] = datetime.now()
        print('printing events  - ', store_events)
        insert_query = events.insert().values(store_events)
        events_id = await database.execute(insert_query)
        result = data_dict

    except Exception as e:
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.get("/events",status_code=status.HTTP_200_OK, tags=["Lotuspay Events"])
async def get_events(
    event_id:str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/events/{event_id}'
    events_response = requests.get(url, auth=(api_key, ''))
    events_dict = response_to_dict(events_response)
    return events_dict  


@router.get("/events_list",status_code=status.HTTP_200_OK, tags=["Lotuspay Events"])
async def get_events_list(
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/events/'
    events_response = requests.get(url, auth=(api_key, ''))
    events_dict = response_to_dict(events_response)
    return events_dict         