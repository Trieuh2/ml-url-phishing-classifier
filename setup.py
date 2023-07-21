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
    # 'punycode',
    # 'port',
    # 'tld_in_path',
    # 'tld_in_subdomain',
    # 'abnormal_subdomain',
    'prefix_suffix',
    'shortening_service',
    'domain_in_brand',
    # 'brand_in_subdomain',
    # 'brand_in_path',
    'suspicious_tld',
    'statistical_report'
]

# Statistical URL features
statistical_features = [
    'length_url',
    'length_hostname',
    'nb_dots',
    'nb_hyphens',
    # 'nb_at',
    'nb_qm',
    'nb_and',
    # 'nb_or',
    'nb_eq',
    'nb_underscore',
    # 'nb_tilde',
    # 'nb_percent',
    'nb_slash',
    # 'nb_star',
    # 'nb_colon',
    # 'nb_comma',
    # 'nb_semicolon',
    # 'nb_dollar',
    # 'nb_space',
    'nb_www',
    'nb_com',
    # 'nb_dslash',
    # 'http_in_path',
    'ratio_digits_url',
    'ratio_digits_host',
    'nb_subdomains',
    'nb_redirection',
    # 'nb_external_redirection',
    'length_words_raw',
    'char_repeat',
    'shortest_words_raw',
    'shortest_word_host',
    'shortest_word_path',
    'longest_words_raw',
    'longest_word_host',
    'longest_word_path',
    'avg_words_raw',
    'avg_word_host',
    'avg_word_path',
    'phish_hints'
]

selected_features = structural_features + statistical_features
target_header = 'status'
pos_label = 'legitimate' # Positive label used for the confusion matrix

# ====================================================================================================
# 1. Preprocess the data
# ====================================================================================================
dp.preprocess_data(raw_data_filepath, selected_features, target_header)

# ====================================================================================================
# 2. Visualize the data
# ====================================================================================================
if (len(structural_features) > 0):
    dv.visualize_structural_feature_distribution(transformed_dataset_filepath, structural_features, target_header)
    dv.visualize_feature_correlation(transformed_dataset_filepath, 'structural', structural_features, target_header)
if (len(statistical_features) > 0):
    dv.visualize_statistical_feature_distribution(transformed_dataset_filepath, statistical_features, target_header)
    dv.visualize_feature_correlation(transformed_dataset_filepath, 'statistical', statistical_features, target_header)

# ====================================================================================================
# # 3. Create an untuned model
# ====================================================================================================
print('untuned model:')
untuned_trained_model = create_model(train_validation_dataset_filepath, target_header, None)
untuned_training_results = evaluate_model(untuned_trained_model, testing_dataset_filepath, target_header, pos_label)

# ====================================================================================================
# 4. Find best hyperparameter settings
# ====================================================================================================
best_hp_settings = find_best_hyperparameter(train_validation_dataset_filepath, target_header)
print('\nbest hyperparameter settings:' + str(best_hp_settings))

# ====================================================================================================
# 5. Create a tuned model
# ====================================================================================================
print('\ntuned model:')
tuned_trained_model = create_model(train_validation_dataset_filepath, target_header, best_hp_settings)
tuned_training_results = evaluate_model(tuned_trained_model, testing_dataset_filepath, target_header, pos_label)

# ====================================================================================================
# 6. Visualize feature importance
# ====================================================================================================
tuned_trained_model = load_model('models/tuned_model.joblib')
dv.visualize_feature_importance(tuned_trained_model, train_validation_dataset_filepath, target_header)

# ====================================================================================================
# 7. Classify random URL
# ====================================================================================================
tuned_trained_model = load_model('models/tuned_model.joblib')
phishing_url = "http://shadetreetechnology.com/V4/validation/a111aedc8ae390eabcfa130e041a10a4" # Retrieved from /datasets/raw_dataset.csv

print('Classifying URL: ' + phishing_url)
result = classify_url(tuned_trained_model, structural_features, statistical_features, phishing_url)

if isinstance(result, tuple):
    vector, prediction = result
    print(f"Classification: {prediction}")
else:
    print('Result: ' + result)

print('\nEnd of program.')