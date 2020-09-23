from pipeline import *

p = Pipeline('data.parquet.gzip', 'Peru')
p.run()