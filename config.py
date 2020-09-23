credentials = {
    "db": {
        "host": "redis",
        "port": 6379
    },
    "data": {
        "country": "Peru",
        "path": "data.parquet.gzip",
        "segments": {
            "frequent_segment": {
                "ranges": [[0, 4], [5,13], [13,37]],
                "column": "total_orders"
            },
            "recency_segment": {
                "ranges": [[30,60], [60,90], [90,120], [120,180], [181, 181]],
                "column": "days_between_orders"
            }
        },
        "default_voucher": "1000"
    }
}