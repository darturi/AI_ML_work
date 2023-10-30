import csv
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Load csv data into a pandas dataframe
    shopping_df = pd.read_csv(filename)
    # Create a dictionary with column names as keys being mapped to
    # empty lists as values
    col_dict = {var: [] for var in shopping_df.columns}

    # A list of column names to be converted to integers
    int_list = ["Administrative", "Informational", "ProductRelated",
                "OperatingSystems", "Browser", "Region", "TrafficType",
                "Weekend", "Revenue"]
    # A list of column names to be converted to floats
    float_list = ["Administrative_Duration", "Informational_Duration",
                  "ProductRelated_Duration", "BounceRates", "ExitRates",
                  "PageValues", "SpecialDay"]
    # A dictionary to convert month names to integer values
    month_dict = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, June=6, Jul=7,
                      Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)

    # Fill the dictionary with the columns meant to be integers as integers
    for header in int_list:
        col_dict[header] = shopping_df[header].astype(np.int64)
    # Fill the dictionary with the columns meant to be float as float
    for header in float_list:
        col_dict[header] = shopping_df[header].astype(np.float64)

    # Fill the value of the "Month" key with integer values representing month
    # numbers as interpreted from month_dict
    col_dict["Month"] = [month_dict[elem] for elem in shopping_df["Month"]]
    # Replace visitor tags with either 0 or 1 and load that data into the
    # correct place in col_dict
    col_dict["VisitorType"] = [1 if elem == "Returning_Visitor" else 0
                               for elem in shopping_df["VisitorType"]]

    # Create the lists to iteratively add to and later be returned
    evidence = []
    labels = []
    # Loop through the rows of the dataframe
    for i in range(len(shopping_df["Month"])):
        temp_list = []
        # For each row take the values of the dict associated with each data
        # point in the original order
        for key in col_dict.keys():
            temp_list.append(col_dict[key][i])
        # Add all but the last element of the list to evidence
        evidence.append(temp_list[:-1])
        # Add the last element of the list to the label list
        labels.append(temp_list[-1])

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Define the model we are using from sklearn
    model = KNeighborsClassifier(n_neighbors=1)
    # Pass the evidence and label lists created in the load_data function
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Establish counts for total correct classifications of
    # purchases and non purchases
    sen_count = 0
    spec_count = 0
    # Loop through the label and prediction lists together
    # by zipping them together
    for label, prediction in zip(labels, predictions):
        # If the person did make a purchase that was predicted
        # by the model increment sen_count
        if label == 1 and label == prediction:
            sen_count += 1
        # If the person did not make a purchase and that was predicted
        # by the model increment spec_count
        elif label == 0 and label == prediction:
            spec_count += 1

    # Perform division to calculate fraction of correct classifications
    # in comparison to total purchases/non-purchases
    sensitivity = sen_count / labels.count(1)
    specificity = spec_count / labels.count(0)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
