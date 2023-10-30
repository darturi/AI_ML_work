import csv
import pandas as pd
import numpy as np

shopping_df = pd.read_csv("shopping.csv")
col_dict = {var: [] for var in shopping_df.columns}

int_list = ["Administrative", "Informational", "ProductRelated",
            "OperatingSystems", "Browser", "Region", "TrafficType",
            "Weekend", "Revenue"]
float_list = ["Administrative_Duration", "Informational_Duration",
              "ProductRelated_Duration", "BounceRates", "ExitRates",
              "PageValues", "SpecialDay"]
month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

for header in int_list:
    col_dict[header] = shopping_df[header].astype(np.int64)
for header in float_list:
    col_dict[header] = shopping_df[header].astype(np.float64)

col_dict["Month"] = [month_dict[elem] for elem in shopping_df["Month"]]
col_dict["VisitorType"] = [1 if elem == "Returning_Visitor" else 0
                           for elem in shopping_df["VisitorType"]]

evidence = []
labels = []
for i in range(len(shopping_df["Month"])):
    temp_list = []
    for key in col_dict.keys():
        temp_list.append(col_dict[key][i])
    evidence.append(temp_list[:-1])
    labels.append(temp_list[-1])
