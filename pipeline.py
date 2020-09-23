import redis
import time
from dataloader import DataLoader
from config import credentials
import logging

logging.basicConfig(level=logging.INFO)


class Pipeline:

    def __init__(self, path, country):

        self.database = redis.Redis(credentials['db']['host'])
        self.segments = credentials["data"]["segments"].keys()
        self.dataloader = DataLoader(path, country)

    def save_to_db(self, key, value):

        self.database.set(key, value)

    def run(self):

        try:
            self.dataloader.load_data()
            logging.info("data has been loaded")
        except:
            logging.error("Can't load the data")
        try:
            self.dataloader.orders_preprocess()
            logging.info("preprocessed orders and days between orders")
        except:
            logging.error("can't preprocess orders or days between last order")

        try:
            self.dataloader.process_empty_vouchers()
            logging.info("preprocessed empty vouchers")
        except:
            logging.error("Can't fill empty vouchers")
        try:
            self.dataloader.fill_segments()
            logging.info("filled up segment variants for the data")
        except:
            logging.error("can't process segments")

        logging.info("saving to db")
        for segment in self.segments:

            for idx, row in self.dataloader.group_to_write(segment, segment + "_variant").iterrows():
                try:
                    self.save_to_db((row[segment] + ":" + row[segment + "_variant"]), row['voucher_amount'])
                    logging.info("saved chunk of the data")
                except:
                    logging.error("Error saving to db")
                time.sleep(2)


