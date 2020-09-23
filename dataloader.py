import pandas as pd
from config import credentials
import logging

logging.basicConfig(level=logging.INFO)


class DataLoader:

    def __init__(self, path, country):

        self.path = path
        self.country = country
        self.data = None

    def load_data(self):

        try:
            logging.info(self.path)
            self.data = pd.read_parquet(self.path)
            self.data = self.data[self.data.country_code == self.country]
        except:
            self.logger.error("Path is invalid")

    # function for calculating days between orders and processing total orders

    def orders_preprocess(self):
        logging.info("Processing orders")
        # delta between event time and last order
        self.data['days_between_orders'] = (pd.to_datetime(self.data['timestamp']) -
                                            pd.to_datetime(self.data['last_order_ts'])).dt.days

        # as some event timestamp less than last order time we filter it out
        self.data = self.data[self.data.days_between_orders >= 0]

        # total orders has str type and empty values, so process it to fill with zeroes
        self.data['total_orders'] = self.data['total_orders'].replace(r'^\s*$', float(0), regex=True)
        self.data['total_orders'] = self.data['total_orders'].astype(float)

        return self.data

    def process_empty_vouchers(self):

        self.data['voucher_amount'].fillna((self.data['voucher_amount'].mean()), inplace=True)

        return self.data

    def segments_processing(self, row, segment_name, segment_variant, ranges, column):

        for x, y in ranges:

            if x <= row[column] < y:
                row[segment_variant] = str(x) + "-" + str(y)
            elif x == y and x <= row[column]:
                row[segment_variant] = str(x) + "+"

        row[segment_name] = segment_name

        return row

    def fill_segments(self):

        segments = credentials["data"]["segments"]
        for segment in segments.keys():
            self.data[segment] = ""

            self.data[segment + "_variant"] = ""

        for segment in segments.keys():
            self.data = self.data.apply(
                lambda row: self.segments_processing(row, segment, segment + "_variant", segments[segment]['ranges'],
                                                     segments[segment]['column']), axis=1)

        return self.data

    def group_to_write(self, segment, variant):

        # filter out data with no segment variant assigned
        return self.data[self.data[variant] != ""].groupby([segment, variant], as_index=False)['voucher_amount'].mean()
