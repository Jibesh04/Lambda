import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def logger_decorator(handler):
    def wrapper(event, context, *args, **kwargs):
        logger.info("Log before the handler")
        response = handler(event, context, *args, **kwargs)
        logger.info("Log after the handler")
        return response
    return wrapper

import json

def request_body_assert_decorator(required_params):
    def decorator(handler):
        def wrapper(event, context, *args, **kwargs):
            body = json.loads(event.get('body', '{}'))
            missing_params = [param for param in required_params if param not in body]
            if missing_params:
                return {
                    'statusCode': 400,
                    'body': f'Missing required parameters: {", ".join(missing_params)}'
                }
            return handler(event, context, *args, **kwargs)
        return wrapper
    return decorator

def parameter_validation_decorator(validations):
    def decorator(handler):
        def wrapper(event, context, *args, **kwargs):
            body = json.loads(event.get('body', '{}'))
            for param, validation in validations.items():
                if param in body:
                    if not validation['type'](body[param]):
                        return {
                            'statusCode': 400,
                            'body': f'Invalid type for parameter: {param}'
                        }
                    if 'encoding' in validation and not isinstance(body[param], str):
                        return {
                            'statusCode': 400,
                            'body': f'Parameter {param} must be a base64 encoded string'
                        }
            return handler(event, context, *args, **kwargs)
        return wrapper
    return decorator

import base64
import pandas as pd
from io import BytesIO

def excel_decoder_decorator(handler):
    def wrapper(event, context, *args, **kwargs):
        body = json.loads(event.get('body', '{}'))
        encoded_excel = body['file']
        decoded_excel = base64.b64decode(encoded_excel)
        df = pd.read_excel(BytesIO(decoded_excel))
        return handler(event, context, df, *args, **kwargs)
    return wrapper

@logger_decorator
@request_body_assert_decorator(required_params=['file'])
@parameter_validation_decorator(validations={'file': {'type': lambda x: isinstance(x, str), 'encoding': 'base64'}})
@excel_decoder_decorator
def lambda_handler(event, context, df):
    unique_values = df['segment'].value_counts().to_dict()
    return {
        'statusCode': 200,
        'body': json.dumps(unique_values)
    }
import base64

def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

if __name__ == "__main__":
    file_path = '/home/jibesh/test/decorator-middy-alternative/scripts/data/excel.xlsx'
    b64_encoded = encode_file_to_base64(file_path)
    event = {
        'body': json.dumps({'file': b64_encoded})
    }
    from pprint import pprint
    pprint(lambda_handler(event, None))