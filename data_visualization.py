import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Function to load CSV data at the given filepath
def load_data(csv_filepath):
    data = pd.read_csv(csv_filepath)
    data = data.reset_index(drop=True)  

    return data

# Function to visualize the binary features' distribution per class
def visualize_binary_feature_distribution(transformed_dataset_filepath, binary_features, target_header):
    # Load the dataset into a DataFrame
    df = load_data(transformed_dataset_filepath)

    # Drop all features that are not binary
    df = df[binary_features + [target_header]]

    # Replace zeros in the dataset with NaNs (preparing for counting feature presence)
    df = df.replace(0, pd.NaT)

    # Compute count of each feature grouped by each class
    grouped_df = df.groupby(target_header).count().T

    # Plot data
    fd_plot = grouped_df.plot(kind='bar', stacked=True, figsize=(15, 6))

    # Set y-limits of the plot to ensure labels fit within the figure
    plt.ylim(0, grouped_df.values.max() * 2.05)

    # Get the count of each feature for each class
    legitimate_counts = grouped_df['legitimate'].tolist()
    phishing_counts = grouped_df['phishing'].tolist()

    # Get the number of features in the dataset
    num_features = len(binary_features)

    # Iterate over the lists of counts and add text labels to the bar plots 
    # to represent the count of each feature being present in each class
    for i in range(num_features):
        # Get the 'legitimate' and 'phishing' count for the current feature
        legitimate_count = legitimate_counts[i]
        phishing_count = phishing_counts[i]
        
        # Calculate the y-coordinate for the text (on top of the stacked bars)
        y_coordinate = (legitimate_count + phishing_count) + (grouped_df.values.max() * 0.05)
        
        # Create the text label in the format of '(legitimate_count, phishing_count)'
        text_label = f'({legitimate_count}, {phishing_count})'
        
        # Add the text label to the bar plot at the specified x and y coordinates
        # The x-coordinate is the count 'i', and the text is horizontally aligned at the center
        fd_plot.text(i, y_coordinate, text_label, ha='center')

    # Set title
    plt.title('Count of Binary Features Across URL Classes', pad=20)

    # Set and pad y-label for visibility
    plt.ylabel('Count', rotation=0, labelpad=40)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.4)

    # Add a text box explaining the value format
    explanation_text = 'Each stacked bar represents the count of instances where the binary feature is present (1) for each class. \n\nFormat: (Legitimate Count, Phishing Count)'
    plt.gcf().text(0.02, 0.02, explanation_text, fontsize=12)

    # Save the plot as a PNG image
    dataset_filename = transformed_dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_binary_feature_distribution.png', dpi=300)

    return None

# Function to visualize the numerical features' distribution per class
def visualize_numerical_feature_distribution(transformed_dataset_filepath, numerical_features, target_header):
    # Load the dataset into a DataFrame
    df = load_data(transformed_dataset_filepath)

    # Drop all features that are not numerical
    df = df[numerical_features + [target_header]]

    # Compute mean value of each feature grouped by each class
    grouped_df = df.groupby(target_header).mean().round(2).T

    # Plot data
    fd_plot = grouped_df.plot(kind='bar', stacked=True, figsize=(15, 6), color=['seagreen', 'orange'])

    # Set y-limits of the plot to ensure labels fit within the figure
    plt.ylim(0, grouped_df.values.max() * 2.05)

    # Get the count of each feature for each class
    legitimate_counts = grouped_df['legitimate'].tolist()
    phishing_counts = grouped_df['phishing'].tolist()

    # Get the number of features in the dataset
    num_features = len(numerical_features)

    # Iterate over the lists of counts and add text labels to the bar plots 
    # to represent the count of each feature being present in each class
    for i in range(num_features):
        # Get the 'legitimate' and 'phishing' count for the current feature
        legitimate_count = legitimate_counts[i]
        phishing_count = phishing_counts[i]
        
        # Calculate the y-coordinate for the text (on top of the stacked bars)
        y_coordinate = (legitimate_count + phishing_count) + (grouped_df.values.max() * 0.05)
        
        # Create the text label in the format of '(legitimate_count, phishing_count)'
        text_label = f'({legitimate_count}, {phishing_count})'
        
        # Add the text label to the bar plot at the specified x and y coordinates
        # The x-coordinate is the count 'i', and the text is horizontally aligned at the center
        fd_plot.text(i, y_coordinate, text_label, ha='center')

    # Set title
    plt.title('Mean Value of Numerical Features Across URL Classes', pad=20)

    # Set and pad y-label for visibility
    plt.ylabel('Mean Value', rotation=0, labelpad=40)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.4)

    # Add a text box explaining the value format
    explanation_text = 'Each stacked bar represents the distribution of the numerical feature\nbased on the mean value across both classes.\n\nFormat: (Legitimate Mean Value, Phishing Mean Value)'
    plt.gcf().text(0.02, 0.02, explanation_text, fontsize=12)

    # Save the plot as a PNG image
    dataset_filename = transformed_dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_numerical_feature_distribution.png', dpi=300)

    return None

# Function to visualize binary feature correlation via heatmap
def visualize_feature_correlation(transformed_dataset_filepath, feature_type, selected_features, target_header):
    # Load the dataset into a DataFrame
    df = load_data(transformed_dataset_filepath)

    # Drop all features that are not binary
    df = df[selected_features + [target_header]]

    # Compute correlation matrix
    corr_matrix = df.corr()

    # Create a large figure to allow enough space for the heatmap
    plt.figure(figsize=(12, 6))

    # Set title
    plt.title('Correlation Matrix of ' + feature_type + ' Features', pad=20)

    # Plot data
    corr_plot = sns.heatmap(corr_matrix, annot=True)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.25)

    # Save the plot as a PNG image
    dataset_filename = transformed_dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_' + feature_type + '_feature_correlation.png', dpi=300)

    return None

# Function to visualize the feature importance of a provided model
def visualize_feature_importance(model, train_validation_dataset_filepath, target_header):
    # Load and split the feature and target data
    X_train = load_data(train_validation_dataset_filepath)
    X_train = X_train.drop(columns=[target_header])

    # Create a series containing feature importances from the model and feature names from the training data
    feature_importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)

    # Create a large figure to allow enough space for the feature importance plot
    plt.figure(figsize=(10, 6))

    # Plot the data
    barplot = sns.barplot(x=feature_importances.values, y=feature_importances.index, palette='crest')

    # Set x-limits of the plot to ensure labels fit within the figure
    plt.xlim(0, max(feature_importances.values) * 1.1)

    # Annotate the feature importance values adjacent to each bar
    for index, value in enumerate(feature_importances):
        barplot.text(value + 0.0005, index + 0.25, str(round(value, 3)))

    # Set title
    plt.title('URL Feature Importances', pad=20)

    # Set and pad y-label for visibility
    plt.ylabel('Feature', rotation=90, labelpad=5)
    plt.xlabel('Relative Importance', labelpad=5)

    # Adjust the margins of the plot
    plt.subplots_adjust(left=0.2)

    # Save the plot as a PNG image
    plt.savefig('visualizations/test_feature_importance.png', dpi=300)

    return None