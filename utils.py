from datetime import datetime
from config import *


def process_request(db, params):
    try:
        days_between_orders = datetime.now() - datetime.strptime(params['last_order_ts'], '%Y-%m-%d %H:%M:%S')
        params['days_between_orders'] = days_between_orders.days

        if params['segment_name'] in credentials['data']['segments']:

            column = credentials['data']['segments'][params['segment_name']]['column']
            ranges = credentials['data']['segments'][params['segment_name']]['ranges']
            found = False

            for x, y in ranges:
                if x <= params[column] < y:
                    if db.get(params['segment_name'] + ":" + str(x) + "-" + str(y)) is not None:
                        found = True
                        return {'voucher': float(db.get(params['segment_name'] + ":" + str(x) + "-" + str(y)))}
            if not found:
                return {'voucher': credentials['data']['default_voucher']}
        return {'voucher': 0}
    except:
        return {'error': 'provide a valid request'}
