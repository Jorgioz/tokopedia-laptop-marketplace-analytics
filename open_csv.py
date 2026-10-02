import pandas as pd
import datetime
import os
import keywords

pd.options.display.max_rows = 240
pd.options.display.min_rows = 240
# pd.options.display.max_columns = 20
data = pd.read_csv("tokopedia_raw_dataset.csv")
print(data)