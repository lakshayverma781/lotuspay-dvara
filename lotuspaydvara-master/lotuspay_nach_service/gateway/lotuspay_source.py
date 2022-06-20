from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.commons import get_env_or_fail, get_env


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_post_source(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=(api_key, ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result


async def lotus_pay_post_source2(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=(api_key, ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result


async def lotus_pay_post_source3(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result


async def lotus_pay_source_status(source_id):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/sources/{source_id}'
        str_url = str(url)
        source_context_response = requests.get(url, auth=(api_key, ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('mandate')
        log_id = await insert_logs(str_url, 'LOTUSPAY', 'GET SOURCE STATUS', source_context_response.status_code,
                                   source_context_response.content, datetime.now())

        result = source_context_response_id
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', 'GET SOURCE STATUS', source_context_response.status_code,
                                   source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result


async def lotus_pay_post_source5(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        # creditor_utility_code = get_env(LOTUSPAY_SERVER, "creditor-utility-code", None)
        # creditor_agent_code = get_env(LOTUSPAY_SERVER, "creditor-agent-code", None)
        # if creditor_utility_code and creditor_agent_code:
        #     data["nach_debit"]["creditor_utility_code"] = creditor_utility_code
        #     data["nach_debit"]["creditor_agent_code"] = creditor_agent_code
        url = validate_url + f'/{context}'
        str_url = str(url)
        str_data = str(data)
        print(str_data)
        source_context_response = requests.post(url, json=data, auth=(api_key, ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        print("==============",url)
       
        print("================response",source_context_dict)

        print('====================source_context_response_id',source_context_response_id)
        log_id = await insert_logs(str_url, 'LOTUSPAY' , str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        # if perdix:
        #     result=source_context_dict
        # else:
        #     result= source_context_response_id
        
        result= source_context_response_id
        print("-------------",result)
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
        print('---------------------==00',result)
    return result



async def lotus_pay_post_sourcewithdraw(context, source_id):
    """ Generic Get Method for lotuspay listing specific source withdraw for a specific customer"""
    try:
        print("coming inside source withdraw")
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/{source_id}/withdraw'
        print(f"------url----- = {url}")
        str_url=str(url)
        # str_data=str(data)
        sourcewithdraw_context_response = requests.post(url,  auth=(api_key, ''))
        print(f" -----------------------{sourcewithdraw_context_response}")
        sourcewithdraw_context_dict = response_to_dict(sourcewithdraw_context_response)
        print(f"----------sourcewithdraw_context_dict-----{sourcewithdraw_context_dict}")
        source_context_response_id = sourcewithdraw_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY',  sourcewithdraw_context_response.status_code,
                                   sourcewithdraw_context_response.content, datetime.now())
        result = source_context_response_id
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY',  sourcewithdraw_context_response.status_code,
                                   sourcewithdraw_context_response.content, datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
        return result