import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Function to load CSV data at the given filepath
def load_data(csv_filepath):
    data = pd.read_csv(csv_filepath)
    data = data.reset_index(drop=True)  

    return data

# Function to visualize the binary features' distribution per class
def visualize_binary_feature_distribution(dataset_filepath, binary_features, target_header):
    # Load the dataset into a DataFrame
    df = load_data(dataset_filepath)

    # Drop all features that are not binary
    df = df[binary_features + [target_header]]

    # Replace zeros in the dataset with NaNs (preparing for counting feature presence)
    df = df.replace(0, pd.NaT)

    # Compute count of each feature grouped by each class
    grouped_df = df.groupby(target_header).count().T

    # Plot data
    fd_plot = grouped_df.plot(kind='bar', stacked=True, figsize=(12, 6))

    # Get the count of each feature for each class
    legitimate_counts = grouped_df['legitimate'].tolist()
    phishing_counts = grouped_df['phishing'].tolist()

    # Get the number of features in the dataset
    num_features = df.shape[1] - 1 # Subtract 1 to account for the 'status' column

    # Iterate over the lists of counts and add text labels to the bar plots 
    # to represent the count of each feature being present in each class
    for i in range(num_features):
        # Get the 'legitimate' and 'phishing' count for the current feature
        legitimate_count = legitimate_counts[i]
        phishing_count = phishing_counts[i]
        
        # Calculate the y-coordinate for the text (on top of the stacked bars)
        y_coordinate = (legitimate_count + phishing_count) * 1.01
        
        # Create the text label in the format of '(legitimate_count, phishing_count)'
        text_label = f'({legitimate_count}, {phishing_count})'
        
        # Add the text label to the bar plot at the specified x and y coordinates
        # The x-coordinate is the count 'i', and the text is horizontally aligned at the center
        fd_plot.text(i, y_coordinate, text_label, ha='center')

    # Set title
    plt.title('Count of Binary Features Across URL Classes')

    # Set and move y-label for visibility
    fd_plot.set_ylabel('Count', rotation=0)
    fd_plot.yaxis.set_label_coords(-0.15,0.5)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.3)

    # Add a text box explaining the value format
    explanation_text = 'Each stacked bar represents the distribution of the binary feature\nbased on the count of whether they are present or not in examples.\nFormat: (Legitimate Count, Phishing Count)'
    plt.gcf().text(0.02, 0.02, explanation_text, fontsize=12)

    # Save the plot as a PNG image
    dataset_filename = dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_binary_feature_distribution.png', dpi=300)

    return None

# Function to visualize the numerical features' distribution per class
def visualize_numerical_feature_distribution(dataset_filepath, numerical_features, target_header):
    # Load the dataset into a DataFrame
    df = load_data(dataset_filepath)

    # Drop all features that are not numerical
    df = df[numerical_features + [target_header]]

    # Compute mean value of each feature grouped by each class
    grouped_df = df.groupby(target_header).mean().round(2).T

    # Plot data
    fd_plot = grouped_df.plot(kind='bar', stacked=True, figsize=(12, 6), color=['seagreen', 'orange'])

    # Get the count of each feature for each class
    legitimate_counts = grouped_df['legitimate'].tolist()
    phishing_counts = grouped_df['phishing'].tolist()

    # Get the number of features in the dataset
    num_features = df.shape[1] - 1 # Subtract 1 to account for the 'status' column

    # Iterate over the lists of counts and add text labels to the bar plots 
    # to represent the count of each feature being present in each class
    for i in range(num_features):
        # Get the 'legitimate' and 'phishing' count for the current feature
        legitimate_count = legitimate_counts[i]
        phishing_count = phishing_counts[i]
        
        # Calculate the y-coordinate for the text (on top of the stacked bars)
        y_coordinate = (legitimate_count + phishing_count) * 1.01
        
        # Create the text label in the format of '(legitimate_count, phishing_count)'
        text_label = f'({legitimate_count}, {phishing_count})'
        
        # Add the text label to the bar plot at the specified x and y coordinates
        # The x-coordinate is the count 'i', and the text is horizontally aligned at the center
        fd_plot.text(i, y_coordinate, text_label, ha='center')

    # Set title
    plt.title('Mean Value of Numerical Features Across URL Classes')

    # Set and move y-label for visibility
    fd_plot.set_ylabel('Mean Value', rotation=0)    
    fd_plot.yaxis.set_label_coords(-0.15,0.5)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.3)

    # Add a text box explaining the value format
    explanation_text = 'Each stacked bar illustrates the distribution of the numerical feature\nbased on the mean value across both classes.'
    plt.gcf().text(0.02, 0.02, explanation_text, fontsize=12)

    # Save the plot as a PNG image
    dataset_filename = dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_numerical_feature_distribution.png', dpi=300)

    return None

# Function to visualize binary feature correlation via heatmap
def visualize_feature_correlation(dataset_filepath, feature_type, selected_features, target_header):
    # Load the dataset into a DataFrame
    df = load_data(dataset_filepath)

    # Drop all features that are not binary
    df = df[selected_features + [target_header]]

    # Compute correlation matrix
    corr_matrix = df.corr()

    # Create a large figure to allow enough space for the heatmap
    plt.figure(figsize=(12, 6))

    # Set title
    plt.title('Correlation Matrix of ' + feature_type + ' Features')

    # Plot data
    corr_plot = sns.heatmap(corr_matrix, annot=True)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.25)

    # Save the plot as a PNG image
    dataset_filename = dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_' + feature_type + '_feature_correlation.png', dpi=300)

    return None