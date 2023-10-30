import csv

with open("shopping.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    col_names = []
    for row in reader:
        col_names.append(row)
        break
    col_names = [col_name for col_name in col_names[0].keys()]

    month_converter = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
                       'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
    int_list = ["Administrative", "Informational", "ProductRelated", "Month", "OperatingSystems",
                "Browser", "Region", "TrafficType"]
    bool_conversion = {"TRUE": 1, "FALSE": 0, "Returning_Visitor": 1, "New_Visitor": 0, "Other":0}
    bool_list = ["VisitorType", "Weekend", "Revenue"]

    col_dict = {}
    for row in reader:
        for col in col_names:
            if col not in col_dict:
                col_dict[col] = [row[col]]
            else:
                col_dict[col].append(row[col])

    for col in col_dict:
        if col in bool_list:
            col_dict[col] = [bool_conversion[ans] for ans in col_dict[col]]
        elif col == "Month":
            col_dict[col] = [month_converter[ans] for ans in col_dict[col]]
        elif col in int_list:
            col_dict[col] = [int(elem) for elem in col_dict[col]]
        else:
            col_dict[col] = [float(elem) for elem in col_dict[col]]

    evidence = []
    labels = []
    for i in col_dict.values():
        print(i)
        input()

    for index in range(len(col_dict.values())):
        print(index)
        temp_list = []
        for row in col_dict.values():
            temp_list.append(row[index])
        print(temp_list)
        input()
