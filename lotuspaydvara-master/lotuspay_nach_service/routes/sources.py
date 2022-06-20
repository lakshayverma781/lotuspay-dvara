
import logging
import re
from fastapi import APIRouter, Depends, status, UploadFile ,File ,Form
from fastapi.responses import JSONResponse, FileResponse,HTMLResponse
from datetime import datetime
import json
from sqlalchemy.sql import text
from databases import Database
from lotuspay_nach_service.resource.generics import response_to_dict
import requests
# import img2pdf
import shutil
import os
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.gateway.lotuspay_source import lotus_pay_post_source, lotus_pay_post_source2, lotus_pay_post_source3, lotus_pay_source_status, lotus_pay_post_source5,lotus_pay_post_sourcewithdraw
from .events_status import get_event_status
from lotuspay_nach_service.data.source_model import (
    sources,
    SourceBase,
    SourceCreate,
    SourceDB,
    Source2Create,
    Source3Create,
    Source5Create,
    sourcewithdraw,
    sourceprocess
)

router = APIRouter()

logger = logging.getLogger("arthmate-lender-handoff-service")

LOTUSPAY_SERVER = 'lotus-pay-server'


async def get_source_or_404(
    source: str,
    database: Database = Depends(get_database)
) -> SourceDB:
    select_query = sources.select().where(sources.c.source_id == source)
    raw_source = await database.fetch_one(select_query)

    if raw_source is None:
        return None

    return SourceDB(**raw_source)


@router.post("/source", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source(
    source: SourceCreate,
    database: Database = Depends(get_database)
) -> SourceDB:

    try:
        source_info = source.dict()
        source_id = source_info.get('source_id')

        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source('sources', source_info)
            if response_source_id is not None:
                get_source_status = await get_event_status(response_source_id)
                source_status = get_source_status['type']
                store_record_time = datetime.now()
                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                save_source['type'] = nach_type
                save_source['source_status'] = source_status
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})

    return result


@router.post("/source/{customer_id}", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def customer_source(
    source2: Source2Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Customer')
        source_info = source2.dict()
        source_id = source_info.get('source_id')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        customer = source_info.get('customer')
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source2('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()

                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                save_source['type'] = nach_type
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                save_source['redirect'] = str_redirect
                save_source['customer'] = customer
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.post("/source/{bank_account}", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_bank_account(
    source3: Source3Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Bank Account')
        source_info = source3.dict()
        print('comingg isndfns')
        print(source_info)
        source_id = source_info.get('bank_account')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        bank_account = source_info.get('bank_account')
        # verify_source_in_db = await get_source_or_404(source_id, database)
        # if verify_source_in_db is None:
        response_source_id = await lotus_pay_post_source3('sources', source_info)
        if response_source_id is not None:
            store_record_time = datetime.now()

            save_source = source_info.get('nach_debit')
            nach_type = source_info.get('type')
            save_source['type'] = nach_type
            save_source['source_id'] = response_source_id
            save_source['created_date'] = store_record_time
            save_source['redirect'] = str_redirect
            save_source['bank_account'] = bank_account
            insert_query = sources.insert().values(save_source)
            source_id = await database.execute(insert_query)

            result = JSONResponse(status_code=200, content={"source_id": response_source_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        # else:
        #     print('Source already exists in DB')
        #     log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
        #                                datetime.now())
        #     result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return "hello"


@router.patch("/source/{source_id}", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def update_source_status(
    source_id: str,
    database: Database = Depends(get_database)
):
    try:

        source_status = await lotus_pay_source_status(source_id)
        if source_status is not None:

            get_source_status = await get_event_status(source_status)
            update_query = sources.select()
            # database.
            testing = await database.execute(update_query)
            print('dkjsafkdjs - ', testing)
            get_mandate_status = get_source_status['type']
            # print('text query', query)
            # source_id = await database.execute(text(query))
            print('printing mandate status from evennts - ', source_status, get_mandate_status)
        # print('coming in main patch request', source_status)

    except Exception as e:
        print(e.args[0])



@router.post("/source5/", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source5(
    source5: Source5Create,
    database: Database = Depends(get_database)) -> SourceDB:
    try:
        print('Coming inside of Customer')
        source_info = source5.dict()
        print(f"---------sourceinfo-----------{source_info}-")
        source_id = source_info.get('source_id')
        print(source_id)
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source5('sources', source_info)
            # print("====re",response_source_id)
            if response_source_id is not None:
                store_record_time = datetime.now()
                nach_debit = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                nach_debit['type'] = nach_type
                nach_debit['source_id'] = response_source_id
                nach_debit['created_date'] = store_record_time
                insert_query = sources.insert().values(nach_debit)
                source_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={
                                      "source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB',  'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={
                                      "message": 'problem with lotuspay parameters'})
        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={
                                  "message": "Source Already Exists in DB"})
        
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={
                              "message": "Error Occurred at DB level"})
    return result


@router.get("/source_PDF", status_code=status.HTTP_200_OK,response_class=HTMLResponse, tags=["Sources"])
async def get_source_pdf(
    source_id : str
    
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = url = validate_url + f'/sources/{source_id}/pdf'
   
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6'
    }
    source_response = requests.get(url, headers=headers, auth=(api_key, ''))
    source_byte=source_response.content
    file_path = os.path.abspath(('./static/'))
    print('------------------PATH',file_path)
    with open ('SC00158UJ9TSUC.pdf','wb') as f :
     

     f.write(source_response.content)
    basename= f.name 
    print('-=================',basename) 
    
    move_item=shutil.copy(basename,file_path)
    print("----------------move",move_item)
    if os.path.exists(move_item):
        remove=os.remove(basename)
        
            
    else :
        print("------file_path------", file_path)
        print("file is not there")
        move_item=shutil.move(basename,file_path)
           

    
    # with open ('SC00158UJ9TSUC.pdf','wb') as f:
    #     f.write(source_response.content)
    #     print ('=======filepath',f)
    #     basename =f.name
    #     print('------------base_path',basename)
    # file_path=os.path.abspath(f) 
    # print ('=======filepath',file_path)
    headers_response={
        "Content-Type": "application/pdf; charset=UTF-8"

    }
    print (file_path)
    return FileResponse(move_item,media_type="application/pdf",filename=basename )
    # return  FileResponse


@router.post("/source_process", tags=["Sources"] )
async def source_proces(
    source_id:str,database: Database = Depends(get_database)
):
    try:

        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url =validate_url + f'/sources/{source_id}/process'
        str_url=str(url)
        headers = {
        'Authorization': 'Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6'
        }
        response = requests.post(url, auth=(api_key, ''))
        print(f"------response----{response}")
        print(f"------response.e----{response.encoding}")
        response_context_dict=response.content
        print(f"------response.content----{response_context_dict}")
    # data=json.load(my_json)
        print(type(response_context_dict))
    # dict_str = response_context_dict.decode("UTF-8")
        response_dict=json.loads(response_context_dict.decode('utf-8'))
        print('===================',response_dict)
        response_id=response_dict.get('id')
        print('----------------ID',response_id)
        store_record_time = datetime.now()
        response_obj=response_dict.get('object')
        response_created=response_dict.get('created')
        
        response_type=response_dict.get('type')
        response_status=response_dict.get('status')
        if response_id is not None:
            source_process_info = {
                'source_withdraw_id': response_id,
                'object': response_obj,
                'created': response_created,
                
                'type': response_type,
                'status':response_status,
                'created_date': store_record_time
            }
            insert_query = sourceprocess.insert().values(source_process_info)
            db_token_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={
                                      "source_process_id": response_id})
        else:
            log_id = await insert_logs(str_url, 'LOTUSPAY', source_id, response.status_code,
                                   response.content, datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})
      
    except Exception as e:
            log_id = await insert_logs(str_url, 'LOTUSPAY', source_id, response.status_code,
                                   response.content, datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result    



@router.post("/source_withdraw", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_withdraw(
    source_id: str,
        database: Database = Depends(get_database)
) -> SourceDB:
    try:
        print("coming inside the source withdraw")
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url =validate_url + f'/sources/{source_id}/withdraw'
        print(f"-------url------{url}")
        str_url=str(url)
        # str_data=str(data)
        sourcewithdraw_context_response = requests.post(url, auth=(api_key, ''))
        print(f"------response----{sourcewithdraw_context_response}")
        # print(f" -----------------------{sourcewithdraw_context_response}")
        sourcewithdraw_context_dict = response_to_dict(sourcewithdraw_context_response)
        print(f"----------sourcewithdraw_context_dict-----{sourcewithdraw_context_dict}")
        source_context_response_id = sourcewithdraw_context_dict.get('id')
        # response_dict=json.loads(sourcewithdraw_context_dict.decode('utf-8'))
        # response_id=response_dict.get('id')
        print('----------------source_context_response_id',source_context_response_id)
        store_record_time = datetime.now()
        response_obj=sourcewithdraw_context_dict.get('object')
        response_created=sourcewithdraw_context_dict.get('created')
        
        response_type=sourcewithdraw_context_dict.get('type')
        response_status=sourcewithdraw_context_dict.get('status')
        if source_context_response_id is not None:
            source_withdraw_info = {
                'source_withdraw_id': source_context_response_id,
                'object': response_obj,
                'created': response_created,
                
                'type': response_type,
                'status':response_status,
                'created_date': store_record_time
            }
            # print(f"--------source_withdraw_info-------{source_withdraw_info}")
            insert_query =sourcewithdraw.insert().values(source_withdraw_info)
            source_id = await database.execute(insert_query)
            print(f"----------{insert_query}")
            result = JSONResponse(status_code=200, content={
                                      "source_id": sourcewithdraw_context_dict})
            log_id = await insert_logs(str_url, 'LOTUSPAY', source_id, sourcewithdraw_context_response.status_code,
                                   sourcewithdraw_context_response.content, datetime.now())
            return result
    except Exception as e:
            log_id = await insert_logs(str_url, 'LOTUSPAY', source_id, sourcewithdraw_context_response.status_code,
                                   sourcewithdraw_context_response.content, datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
            return result

















