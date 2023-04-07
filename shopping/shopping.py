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

    # load dataframe from .csv file
    df = pd.read_csv(filename)

    # create list of labels
    labels = df.pop('Revenue').map(lambda x: 1 if x else 0).to_numpy().tolist()

    # Weekend, an integer 0 (if false) or 1 (if true)
    df.Weekend = df.Weekend.map(lambda x: 1 if x else 0)

    # VisitorType, an integer 0 (not returning) or 1 (returning)
    df.VisitorType = df.VisitorType.map(lambda x: 0 if x == 'New_Visitor' or x == 'Other' else 1)

    # Month, an index from 0 (January) to 11 (December)
    months = {
        "Jan"   : 0,
        "Feb"   : 1,
        "Mar"   : 2,
        "Apr"   : 3,
        "May"   : 4,
        "June"  : 5,
        "Jul"   : 6,
        "Aug"   : 7,
        "Sep"   : 8,
        "Oct"   : 9,
        "Nov"   : 10,
        "Dec"   : 11
    }

    df.Month = df.Month.replace(months).astype('int64')

    # convert df values to list, preserving original datatypes
    evidence = list(map(list, df.itertuples(index=False)))

    # return evidences, labels
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    # All positive labels
    actual_positives = [label for label in labels if label == 1]
    # All correct positive predictions
    true_positives = [1 for label, prediction in zip(labels, predictions) if label == 1 and prediction == 1]


    #print("Total positives: ", len(actual_positives))
    #print("Correct Positives: ", sum(true_positives))
    #print("TPR: ", sum(true_positives) / len(actual_positives))

    # all negative labels
    actual_negatives = [label for label in labels if label == 0]
    # all correct negative predictions
    true_negatives = [1 for label, prediction in zip(labels, predictions) if label == 0 and prediction == 0]


    #print("Total negatives: ", len(actual_negatives))
    #print("Correct negatives: ", sum(true_negatives))
    #print("TNR: ", sum(true_negatives) / len(actual_negatives))

    # Calculate sensitivity
    sensitivity = sum(true_positives) / len(actual_positives)
    # Calculate specificity
    specificity = sum(true_negatives) / len(actual_negatives)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
