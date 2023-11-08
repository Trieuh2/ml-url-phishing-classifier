# ml-url-phishing-classifier

## Features
1. ML Model Creation: Trains an ML model selected URL features.
2. ML Model Tuning: Tunes the created ML model with hyperparameter-tuning.
3. URL Classification: Identify if a provided URL is phishing or legitimate
4. Feature Extraction: Parses a URL for structural and statistical data used for analysis.
5. Data Preprocessing: Parses, transforms, and splits a raw dataset into additional datasets used for train-validation and testing the ML model.
6. Data Visualization: Generates graphical plots to illustrate the feature distribution, feature correlation, and feature importance. 

## Introduction
This application is a machine-learning-based phishing URL detection tool designed to classify URLs as legitimate or phishing based on extracted URL features. The underlying model is trained using the Random Forest Classification algorithm based on extracted structural and statistical data. Both structural and statistical data are extracted from links entered into the application and processed by the model for a resulting classification (legitimate/phishing).

Structural features are binary components that identify whether the feature is present or absent within a URL. An example structural feature is 'ip', which indicates whether the main hostname is an IP address or not. The structural features with clearly distinct distributions between each class were selected in order to understand the data better. Using the same example of the 'ip' structural feature, the Structural Feature Distribution visualization indicated that encountering websites with IP addresses as their hostname was more likely to be classified as phishing than legitimate.

Statistical features are non-binary URL components such as the length of a URL, the average words in the path, or the number of slashes in the URL for example. These features are useful to identify trends where particular features are present in both classes but in distinguishable averaged amounts that can help the ML model perform classifications accurately. Within the Statistical Feature Distribution visualization, phishing URLs were found to have much longer URL lengths in comparison to legitimate URLs for example. The mean URL length of phishing URLs was 74.87 and the mean URL length of legitimate URLs was 47.87 from the visualizations included in this repository.

## Getting Started

### Prerequisites
The application requires the following libraries to be installed:
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [NumPy](https://numpy.org/install/)
- [scikit-learn](https://scikit-learn.org/stable/install.html)
- [seaborn](https://seaborn.pydata.org/installing.html)


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

The source dataset is a compilation of 11,430 URLs with extracted features such as the URL length, URL hostname, number of dots, number of hyphens, longest words in the hostname, presence of IP address, and more features. Within the dataset, the 'status' column serves as the ground truth, and the ML model is trained to utilize the extracted features to determine the status of the provided URL. 

The source dataset is balanced with 50% phishing URLs and 50% legitimate URLs. For training and testing, 70% of the raw data was split for training and the remaining 30% of data was used for testing. Within the training and testing datasets, the ratio of class distribution was maintained for a fair assessment.

In the [raw dataset](https://github.com/Trieuh2/ml-url-phishing-classifier/blob/main/datasets/raw_dataset.csv) used in the project, the source dataset is slightly modified to correct typos in the URL feature names.

## Usage

### Basic Usage
1. Run the application in a terminal using 'python app.py'
2. Provide a URL containing "http://" or "https://" for classification.
3. The application will return the classification result 'phishing', 'legitimate', or return an error if the link was not accessible.

### Advanced Usage
The application can be modified to train a new ML model using different selected structural and statistical URL features:
1. Modify the selected features by uncommenting or commenting on the features within the 'structural_features' and 'statistical_features' in the 'setup.py' file.\
\
In the example below, the 'ip', 'https_token', 'prefix_suffix', 'shortening_service', 'domain_in_brand', 'suspicious_tld', and 'statistical_report' features are selected.
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

To run a 'legitimate' URL example, use: "https://www.google.com" or a website you have safely visited before.

To run a 'phishing' URL example, an accessible link can be found via the [raw_dataset.csv](https://github.com/Trieuh2/ml-url-phishing-classifier/blob/main/datasets/raw_dataset.csv) file. The application safely performs feature extraction offline and does not perform any web requests to any links entered into the application.

## Results
After training the ML model on the Random Forest Classification algorithm and performing hyperparameter tuning, the tuned model's evaluation resulted in the performance metrics below.
```
Accuracy: 0.9026239067055394 
Precision: 0.8989023685730791 
Recall: 0.9072886297376094 
Confusion Matrix: 
[[1556  159]
 [ 175 1540]]
```

### Data visualizations
After data preprocessing is performed, data visualizations are created to represent the feature distribution, feature correlation, and feature importance. Since structural features are represented in binary and statistical features are represented numerically, a feature distribution plot and feature correlation matrix heatmap are created for each type of feature (structural/statistical), for each class (phishing/legitimate). A single feature importance plot is used to represent the influence of all selected features.
</br>
</br>
**Feature Distribution**  
The feature distribution for each type of feature (structural/statistical) for each class is represented in a stacked bar plot to identify the presence of each feature within the phishing vs. legitimate URLs. Using this visualization assists with understanding features that would be useful feature candidates for feature selection during improvement iterations. Features that appeared near 1:1 ratios (between phishing and legitimate URLs) were deselected during performance tuning iterations. These deselected features are commented out within the [app.py](https://github.com/Trieuh2/ml-url-phishing-classifier/blob/main/app.py) file.
![Statistical Feature Distribution example visualization](https://github.com/Trieuh2/ml-url-phishing-classifier/blob/main/visualizations/transformed_dataset_statistical_feature_distribution.png)

 
**Feature Correlation Matrix Heatmap**  
The feature correlation matrix heatmap represents how closely correlated a structural feature is related to another structural feature and vice versa for statistical features. Hot areas on the matrix indicate a high correlation which suggests a strong linear relationship between two variables in which an increase in one variable will predictably increase the value of the highly correlated variable as well. When creating and tuning the model, this heatmap was useful to prune redundant features that were selected and minimize the noise for training the model.
![Statistical Feature Correlation Matrix Heatmap example visualization](https://github.com/Trieuh2/ml-url-phishing-classifier/blob/main/visualizations/transformed_dataset_statistical_feature_correlation.png)

**Feature Importance**  
The distribution of feature importance is illustrated in a ranked bar plot, where the selected features are represented on the Y-axis, and the weight of each feature (in relation to classification decisions) is represented on the X-axis. The highest-ranked features correlate to the most reliable features for the model to use when performing classification.
![Feature Importance example visualization](https://github.com/Trieuh2/ml-url-phishing-classifier/blob/main/visualizations/url_feature_importance.png)

## Acknowledgements
The original raw dataset and main feature extraction logic were sourced from the [open-source repository](https://data.mendeley.com/datasets/c2gw7fy2j4/3) created as a result of a [study](https://arxiv.org/abs/2010.12847) performed by Abdelhakim Hannousse and Salima Yahiouche.
