import classification_model as cm
import data_preprocessing as dp
import data_visualization as dv
import feature_extractor as fe
import pandas as pd
import time as t

from classification_model import classify_url, create_model, evaluate_model, find_best_hyperparameter, load_model

# Define dataset paths
raw_data_filepath = 'datasets/raw_dataset.csv'
transformed_dataset_filepath = 'datasets/transformed_dataset.csv'
train_validation_dataset_filepath = "datasets/train_validation_dataset.csv"
testing_dataset_filepath = "datasets/testing_dataset.csv"

# Structural URL features
structural_features = [
    'ip',
    'https_token',
    'punycode',
    'port',
    'tld_in_path',
    'tld_in_subdomain',
    'abnormal_subdomain',
    'prefix_suffix',
    'shortening_service',
    'domain_in_brand',
    'brand_in_subdomain',
    'brand_in_path',
    'suspicious_tld',
    'statistical_report'
]

# Statistical URL features
statistical_features = [
    'length_url',
    # 'length_hostname',
    'nb_dots',
    'nb_hyphens',
    # 'nb_at',
    'nb_qm',
    'nb_and',
    # 'nb_or',
    'nb_eq',
    # 'nb_underscore',
    # 'nb_tilde',
    # 'nb_percent',
    # 'nb_slash',
    # 'nb_star',
    # 'nb_colon',
    # 'nb_comma',
    # 'nb_semicolumn',
    # 'nb_dollar',
    # 'nb_space',
    'nb_www',
    # 'nb_com',
    # 'nb_dslash',
    # 'http_in_path',
    'ratio_digits_url',
    # 'ratio_digits_host',
    # 'nb_subdomains',
    # 'nb_redirection',
    # 'nb_external_redirection',
    # 'length_words_raw',
    'char_repeat',
    # 'shortest_words_raw',
    'shortest_word_host',
    # 'shortest_word_path',
    'longest_words_raw',
    # 'longest_word_host',
    'longest_word_path',
    'avg_words_raw',
    'avg_word_host',
    'avg_word_path',
    'phish_hints'
]

tuned_trained_model = load_model('models/tuned_model.joblib')
exit = False

while not exit:
    # Request for user input to classify a URL
    user_input = input("Enter a URL for classification.\nPlease make sure to include 'http://' or 'https://' in your input.\n(Enter 'exit' to quit the application):\n\t")

    if user_input == "exit":
        break
    else:
        result = classify_url(tuned_trained_model, structural_features, statistical_features, user_input)

        if isinstance(result, tuple):
            vector, prediction = result
            print(f"Classification: {prediction}")
        else:
            print('\nResult: ' + result)
        t.sleep(2)
        print()