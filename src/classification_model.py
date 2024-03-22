import feature_extractor as fe
import pandas as pd
import numpy as np
import joblib as jb

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

# Function that evaluates the provided ML model using the testing dataset
def evaluate_model(model, testing_dataset_filepath, target_header, pos_label, eval_output_filepath):
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
    f1_score = 2 * (precision * recall) / (precision + recall)
    conf_matrix = confusion_matrix(Y_test, Y_pred)

    # Save the evaluation results to a text file
    with open(eval_output_filepath, 'w') as f:
        f.write("Accuracy: " + str(accuracy) + "\n")
        f.write("Precision: " + str(precision) + "\n")
        f.write("Recall: " + str(recall) + "\n")
        f.write("F1-Score: " + str(f1_score) + "\n")
        f.write("Confusion Matrix: " + str(conf_matrix) + "\n")

    return accuracy, precision, recall, f1_score, conf_matrix

# Function that prints out the performance metrics
def print_performance_metrics(accuracy, precision, recall, f1_score, conf_matrix):
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1-Score: ", f1_score)
    print("Confusion Matrix: ", conf_matrix)
    print()


# Function that classifies a given URL using the provided ML model
def classify_url(model, structural_features, statistical_features, url):
    if (url.startswith('http://') or url.startswith('https://')):
        vector = fe.extract_features(url, structural_features, statistical_features)

        if vector is not None and len(vector) > 0:
            prediction = model.predict(vector)
            prediction = str(prediction)

            if prediction == "['phishing']":
                return 'Phishing'
            elif prediction == "['legitimate']":
                return 'Legitimate'
    else:
        return 'Invalid URL'

