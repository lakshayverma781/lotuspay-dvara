
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database 
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.gateway.lotuspay_payments import lotus_pay_payments_post, lotus_pay_payments_cancel
from lotuspay_nach_service.data.payments_model import (
    payments,
    PaymentBase,
    PaymentCreate,
    payments_cancel,
    PaymentDB,
)

LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()


@router.post("/payments", response_model=PaymentDB, status_code=status.HTTP_201_CREATED,  tags=["Payments"])
async def create_payments(
    payments: PaymentCreate, database: Database = Depends(get_database)
) -> PaymentDB:

    try:
        payments_info = payments.dict()
        response_payment_id = await lotus_pay_payments_post('payments', payments_info)
        print(response_payment_id)
        if response_payment_id is not None:
            payment_info = {
                **payment_info,
                'payment_id': response_payment_id,
                'created_date': datetime.now()
            }
            insert_query = payments.insert().values(payment_info)
            payment_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"payment_id": response_payment_id})
        result = response_payment_id

    except:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
    return result








@router.post("/payment_cancellation",   tags=["Payments"])
async def payment_cancellation(
    payment_id: str, database: Database = Depends(get_database)
) -> PaymentDB:

    try:
        print('before posting')
        response_payment_id = await lotus_pay_payments_cancel('payments', payment_id)
        store_record_time = datetime.now()
        print('after posting', response_payment_id)
        if response_payment_id is not None:
            payments_info = {
                'payment_id': response_payment_id,
                'created_date': store_record_time
            }
            insert_query = payments_cancel.insert().values(payments_info)
            db_payment_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"payments_id": response_payment_id})

        # result = response_payment_id
        else:
            log_id = await insert_logs('LOTUSPAY', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": "Error Occurred at LotusPay level"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
    return result 



@router.get("/payment", tags=["Payments"])
async def get_payments(
    payment_id:str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/payments/{payment_id}'
    payment_response = requests.get(url, auth=(api_key, ''))
    payment_dict = response_to_dict(payment_response)
    return payment_dict 




@router.get("/payments_list", tags=["Payments"])
async def get_payment_list(
    limit:int
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/payments?{limit}'
    payment_response = requests.get(url, auth=(api_key, ''))
    payment_dict = response_to_dict(payment_response)
    return payment_dict