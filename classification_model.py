# Data Processing
import pandas as pd
import numpy as np
import joblib as jb

# Modelling
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

# Function loads a CSV, given the filepath
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

# Function loads a dumped joblib ML model, given the filepath
def load_model(model_filepath):
    model = load(model_filepath)
    return model

# Fucntion creates a new ML model, trains it via Random Forest and dumps it 
def create_model(train_validation_dataset_filepath, target_header, custom_hyperparameters):
    tuned_status = ''
    
    # Load and split the feature and target data
    X_train = load_data(train_validation_dataset_filepath)
    X_train = X_train.drop(columns=[target_header])

    Y_train = load_data(train_validation_dataset_filepath)
    Y_train = Y_train[target_header]

    # Create a new model using the Random Forest Classifier and train the model
    if custom_hyperparameters == None:
        model = RandomForestClassifier()
        tuned_status = 'untuned'
    else:
        model = RandomForestClassifier(max_depth=custom_hyperparameters['max_depth'], n_estimators=custom_hyperparameters['n_estimators'])
        tuned_status = 'tuned'

    # Fit the model to the data
    model.fit(X_train, Y_train)

    # Dump the model as a local file that can be referenced again
    dump(model, 'models/' + tuned_status + '_model.joblib')

    return model

# Function that finds the best hyperparameter
def find_best_hyperparameter(train_validation_dataset_filepath, target_header):
    param_dist = {
        'n_estimators': randint(5, 500),
        'max_depth': randint(1, 20)}
    
    # Load and split the feature and target data
    X_train = load_data(train_validation_dataset_filepath)
    X_train = X_train.drop(columns=[target_header])

    Y_train = load_data(train_validation_dataset_filepath)
    Y_train = Y_train[target_header]

    # Create a new model using the Random Forest Classifier and train the model
    model = RandomForestClassifier()
    random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=5, cv=5)

    # Fit the random search object to the data to obtain the best model
    random_search.fit(X_train, Y_train)

    # Print the best model's hyperparameters
    best_rf = random_search.best_estimator_.get_params()

    return best_rf

# Function that evaluates the provided ML model using the testing dataset.
def evaluate_model(model, testing_dataset_filepath, target_header, pos_label):
    # Load and split the feature and target data
    X_test = load_data(testing_dataset_filepath)
    X_test = X_test.drop(columns=[target_header])

    Y_test = load_data(testing_dataset_filepath)
    Y_test = Y_test[target_header]

    # Perform predictions using the model's testing data
    Y_pred = model.predict(X_test)

    # Evaluate the predictions against the testing data's results
    accuracy = accuracy_score(Y_test, Y_pred)
    precision = precision_score(Y_test, Y_pred, pos_label=pos_label)
    recall = recall_score(Y_test, Y_pred, pos_label=pos_label)
    conf_matrix = confusion_matrix(Y_test, Y_pred)

    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("Confusion Matrix: ", conf_matrix)

    return accuracy, precision, recall, conf_matrix