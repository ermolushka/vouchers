import os
from dataloader import *

parentDirectory = os.getcwd()
file_dir = os.path.join(parentDirectory, 'data.parquet.gzip')
d = DataLoader(file_dir, 'Peru')

def test_data_load():
    d.load_data()
    assert len(d.data) != 0

def test_days_between_orders():

    d.orders_preprocess()
    assert len(d.data[d.data.days_between_orders < 0]) == 0

def test_total_orders():

    assert(d.data.total_orders.dtype == float)

def test_empty_vouchers():
    d.process_empty_vouchers()
    assert d.data['voucher_amount'].isnull().sum(axis = 0) == 0

def test_fill_segments():
    segments = credentials["data"]["segments"]

    d.fill_segments()

    assert all([x in d.data.columns for x in segments])










