import matplotlib.pyplot as plt
import pandas as pd

# Function to load CSV data at the given filepath
def load_data(csv_filepath):
    data = pd.read_csv(csv_filepath)
    data = data.reset_index(drop=True)  

    return data

# Function to visualize feature distribution per class via stacked bar plots for each feature
def visualize_feature_distribution(dataset_filepath):
    # Load the dataset into a DataFrame
    df = load_data(dataset_filepath)

    # Replace zeros in the dataset with NaNs (preparing for counting feature presence)
    df = df.replace(0, pd.NaT)

    # Drop the "url" column since it's not a feature
    df = df.drop(columns=['url'])

    # Compute count of each feature grouped by each class
    grouped_df = df.groupby('status').count().T

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
    plt.title('Feature Presence Count Across URL Classes')

    # Set y-label with horizontal rotation
    fd_plot.set_ylabel('Count', rotation=0)

    # Move y-label away from bar graph for visibility
    fd_plot.yaxis.set_label_coords(-0.15,0.5)

    # Rotate x-axis labels to horizontal and set tight layout to prevent overlapping labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adjust subplot parameters to make more space at the bottom
    plt.subplots_adjust(bottom=0.3)

    # Add a text box explaining the value format
    explanation_text = 'Each stacked bar represents a feature.\nNumbers on top of bars are in the format: (Legitimate Count, Phishing Count)'
    plt.gcf().text(0.02, 0.02, explanation_text, fontsize=12)

    # Save the plot as a PNG image
    dataset_filename = dataset_filepath.split('/')[-1]
    dataset_file_prefix = dataset_filename.split('.')[0]
    plt.savefig('visualizations/' + dataset_file_prefix + '_' + 'feature_distribution.png', dpi=300)

    return None