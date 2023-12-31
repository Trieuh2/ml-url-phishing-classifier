import pandas as pd

# Function to create the preprocessed datasets
def preprocess_data(raw_data_filepath, selected_features, target_header):
    raw_data = load_data(raw_data_filepath)
    transformed_data = create_transformed_csv(raw_data, selected_features, target_header)
    split_transformed_data(transformed_data)

# Function to load CSV data at the given filepath
def load_data(csv_filepath):
    data = pd.read_csv(csv_filepath)
    data = data.reset_index(drop=True)  

    return data

# Function to create a new transformed dataset CSV with only the selected columns
def create_transformed_csv(raw_data, selected_features, target_header):
    raw_data.to_csv('datasets/transformed_dataset.csv', columns=(selected_features + [target_header]), index=False)
    transformed_data = load_data('datasets/transformed_dataset.csv')

    return transformed_data

# Function to split the data into train-validation and testing datasets (70-30 split)
def split_transformed_data(transformed_data):
    # Sample each class of the data separately to maintain a consistent class distribution with the original dataset
    phishing_data = transformed_data[transformed_data['status'] == 'phishing']
    legitimate_data = transformed_data[transformed_data['status'] == 'legitimate']

    # Split the phishing data into train-validation and testing datasets
    phishing_train_val_data = phishing_data.sample(frac=0.7, random_state=0)
    phishing_test_data = phishing_data.drop(phishing_train_val_data.index)

    # Split the legitimate data into train-validation and testing datasets
    legitimate_train_val_data = legitimate_data.sample(frac=0.7, random_state=0)
    legitimate_test_data = legitimate_data.drop(legitimate_train_val_data.index)

    # Combine the split phishing and legitimate data into train-validation and testing datasets
    train_val_data = pd.concat([phishing_train_val_data, legitimate_train_val_data])
    test_data = pd.concat([phishing_test_data, legitimate_test_data])

    # Save the train-validation and testing datasets to CSV files
    train_val_data.to_csv('datasets/train_validation_dataset.csv', index=False)
    test_data.to_csv('datasets/testing_dataset.csv', index=False)
    
    return None