# ml-url-phishing-classifier

## Features
1. ML Model Creation: Trains a ML model selected URL features.
2. ML Model Tuning: Tunes the created ML model with hyperparameter-tuning.
3. URL Classification: Identify if a provided URL is phishing or legitimate
4. Feature Extraction: Parses a URL for structural and statistical data used for analysis.
5. Data Preprocessing: Parses, transforms, and splits a raw dataset into additional datasets used for train-validation and testing the ML model.
6. Data Visualization: Generates graphical plots to illustrate the feature distribution, feature correlation, and feature importance. 

## Introduction
This application is a machine-learning-based phishing URL detection tool designed to classify URLs as legitimate or phishing based on extracted URL features. The underlying model is trained using the Random Forest Classification algorithm based on extracted structural and statistical data. Structural data is extracted solely from the URL data as-is and statistical data is extracted from the URL after programmatically accessing and parsing content data from the browsing interaction and final URL structure.

## Getting Started

### Prerequisites
The application requires the following libraries installed:
- pandas
- numpy
- scikit-learn
- seaborn


### Installation
1. Clone the repository using the following command:
```
git clone https://github.com/Trieuh2/ml-url-phishing-classifier/
```
2. Install dependencies using the following pip commands:
```
pip install pandas
pip install numpy
pip install scikit-learn
pip install seaborn
```

## Data
The data used in this project consists of extracted URL features that are used to train an ML model via the Random Forest Classification algorithm to identify URLs as phishing or legitimate. The raw dataset was sourced from Abdelhakim Hannousse and Salima Yahiouche (2021) as part of their open-source research study available [here](https://data.mendeley.com/datasets/c2gw7fy2j4/3). The source dataset is named 'dataset_B_05_2020.csv'.

The source dataset is a compilation of 11,430 URLs with extracted features such as the URL length, URL hostname, number of dots, number of hyphens, longest words in the hostname, presence of IP address, and more features. Within the dataset, the 'status' column serves as the ground truth, and the ML model is trained on utilizing the extracted features to determine the status of the provided URL. 

The source dataset is balanced with 50% phishing URLs and 50% legitimate URLs. For training and testing, 70% of the raw data was split for training and the remaining 30% of data was used for testing. Within the training and testing datasets, the ratio of class distribution was maintained for a fair assessment.

In the raw dataset (/datasets/raw dataset.csv) used in the project, the source dataset is slightly modified to correct typos in the URL feature names.

## Usage

### Basic Usage
1. Run the application in a terminal using 'python app.py'
2. Provide a URL containing "http://" or "https://" for classification.
3. The application will return the classification result 'phishing', 'legitimate', or return an error if the link was not accessible.

### Advanced Usage
The application can be modified to train a new ML model using different selected structural and statistical URL features:
1. Modify the selected features by uncommenting or commenting on the features within the 'structural_features' and 'statistical_features' in the 'setup.py' file.\
\
In the example below, the ip, https_token, prefix_suffix, shortening_service, domain_in_brand, suspicious_tld, and statistical_report features are selected.
      ```
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
      ```
2. Run 'setup.py' to perform the following the following:
    - Overwrite the transformed dataset, train-validation dataset, and testing dataset in the 'datasets' folder
    - Overwrite the feature distribution and feature correlation visualizations in the 'visualizations' folder
    - Overwrite untuned and hyperparameter-tuned models in the 'models' folder
    - Overwrite .txt files containing the untuned and tuned model performance metrics from evaluations in the 'models' folder
3. Select the same features in step 1 but in the 'app.py' file
4. Run 'app.py'
6. Provide a URL containing "http://" or "https://" for classification
7. The application will return the classification result 'phishing', 'legitimate', or return an error if the link was not accessible.

To run a 'legitimate' URL example, use: "https://www.google.com"

(OPTIONAL) To run a 'phishing' URL example, an accessible link can be found via the "raw_dataset_website_accessibility.csv". **Please use phishing links at your own risk as the application programmatically tests access to the provided URL via requests.get().**

## Results
After training the ML model on the Random Forest Classification algorithm and performing hyperparameter tuning, the tuned model's evaluation resulted in the following performance metrics:
'''
Accuracy: 0.9026239067055394
Precision: 0.8989023685730791
Recall: 0.9072886297376094
Confusion Matrix: [[1556  159]
 [ 175 1540]]
'''

### Data visualizations
After data preprocessing is performed, data visualizations are created to represent the feature distribution, feature correlation, and feature importance. Since structural features represent in binary and statistical features are represented numerically, a feature distribution plot and feature correlation matrix heatmap is created for each type of feature (structural/statistical), for each class (phishing/legitimate). A single feature importance plot is used to represent the influence of all selected features.

**Feature Distribution**
The feature distribution for each type of feature (structural/statistical) for each class is represented in a stacked bar plot to understand if structural features appear more or less common in phishings URLs vs. legitimate URLs, and if the value in a statistical feature is typically higher or lower in one class compared to another.
	
**Feature Correlation Matrix Heatmap**
The feature correlation matrix heatmap is used to represent how closely correlated a structural feature is related to another structural feature and vice versa for statistical features. High correlation suggests a strong linear relationship between two variables in which an increase in one variable will predictably increase the value in the highly correlated variable as well (which can identify redundant selected features and also cause performance impact on the ML model).

**Feature Importance**
After creating and training the tuned model, the feature importance is illustrated in a ranked bar plot, used to represent how much each feature is contribution to the final prediction.

## Acknowledgements
The original raw dataset and main feature extraction logic was sourced from the [open-source repository](https://data.mendeley.com/datasets/c2gw7fy2j4/3) created as a result of a [study](https://arxiv.org/abs/2010.12847) performed by Abdelhakim Hannousse and Salima Yahiouche.