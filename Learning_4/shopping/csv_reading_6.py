# Combines 4 and 5

import csv
import pandas as pd
import numpy as np

shopping_df = pd.read_csv("shopping.csv")

month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

row_num = len(shopping_df["Month"])

# Handling the Months Col
months = np.empty(row_num, np.int64)
for row in range(row_num):
    months[row] = month_dict[shopping_df["Month"][row]]
shopping_df["Month"] = months

# Handling the Returning Visitor Col
returning = months
for row in range(row_num):
    if returning[row] == "Returning_Visitor":
        returning[row] = 1
    else:
        returning[row] = 0
shopping_df["VisitorType"] = returning

# Handling Bool to Int Conversion
shopping_df["Weekend"] = shopping_df["Weekend"].astype(np.int64)
shopping_df["Revenue"] = shopping_df["Revenue"].astype(np.int64)

int_list = ["Administrative", "Informational", "ProductRelated", "Month", "OperatingSystems",
            "Browser", "Region", "TrafficType", "VisitorType", "Weekend", "Revenue"]

col_names = list(shopping_df.columns)
col_count = len(col_names)
shop_arr = shopping_df.to_numpy()

shop_arr = shop_arr.astype('object')

for col_num in range(col_count):
    if col_names[col_num] in int_list:
        shop_arr[:, col_num] = shop_arr[:, col_num].astype(np.int64)

solution_list = []
for row in shop_arr:
    row_list = list(row)
    solution_list.append([row_list[:-1], row_list[:1]])