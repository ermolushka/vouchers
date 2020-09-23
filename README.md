## API for processing data and predict voucher amount
To run it (will run tests, pipeline and will start api):

`docker-compose up`

After you can go to `http://0.0.0.0:5000/voucher` and send request like this

```
{
    "customer_id": 123,
    "last_order_ts": "2020-07-30 10:12:13",
    "country_code": "Peru",
    "total_orders": 15,
    "segment_name": "recency_segment"
}
```

The overall architecture consists of several parts:

1) Config files with all variables
2) dataloader - includes data loading, cleaning and processing of the dataframe
- I created column `days_between_orders` which is a difference between timestamp of the event and last order time (some of them may be invalid as event timestamp is less so I filter it out)
- I also filled up invalid `total_orders` values with zeroes
- Some voucher_amount were empty. I was trying different approaches as can be seen in my eda analysis but end up using a simple mean as there were no difference
- Fill segments based on the config file
- For each segment I calculate mean of the vouchers as an approximation to most frequently used
3) pipeline - class for running pipeline
- Init dataloader and db connection and trying to execute data processing
4) utils - to process incoming request
5) Data storage - Redis as amount of data is not huge and we need a fast lookup
6) API - Flask
7) Infra: running two Docker images to handle 
- Flask
- Redis  

Note: here I don't have all possible segments because of the nature of the data. If there is no data in the db for the given payload, I return default value defined in the config.

How I would improve it:
1) Switch API to FastAPI for async work
2) Use Cassandra for data storage and redis as a cache
3) Rebuild pipeline using Airflow to make it resilient
4) With the bigger amount of data would try to use KNN to fill up missing vouchers based on metadata (tried but not useful)
5) More feature generation and probable some ML to make predictions of vouchers more accurate
6) Would add logs monitoring using Kibana
7) Extend pipeline to watch for the new files in the directory and process it 

