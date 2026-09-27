import pandas as pd
import datetime
import os

pd.options.display.max_rows = 240
pd.options.display.min_rows = 240
# pd.options.display.max_columns = 20
data = pd.read_csv("tokopedia_raw_dataset.csv")
print(data)

# print(os.getcwd())

# path = os.getcwd()
# folder_name = "url_product"
# if not os.path.isdir(path + "\\" + folder_name):
#     os.makedirs(path + "\\" + folder_name)
# print(files_name)