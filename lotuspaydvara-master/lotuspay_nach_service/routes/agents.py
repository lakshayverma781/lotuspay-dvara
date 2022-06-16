from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from lotuspay_nach_service.commons import get_env_or_fail

LOTUSPAY_SERVER = 'lotus-pay-server'

router = APIRouter()



@router.get("/agents", tags=["Agents"])
async def get_agents(
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/agents/'
    agents_response = requests.get(url, auth=(api_key, ''))
    agent_dict = response_to_dict(agents_response)
    return agent_dict  


@router.get("/agents_list",status_code=status.HTTP_200_OK, tags=["Agents"])
async def get_agents_list(
    agent_id:str
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/agents/{agent_id}'
    agents_response = requests.get(url, auth=(api_key, ''))
    agent_dict = response_to_dict(agents_response)
    return agent_dict 