import classification_model as cm
import concurrent.futures
import data_preprocessing as dp
import data_visualization as dv
import feature_extractor as fe
import pandas as pd
import random
import requests
import time as t

# This function returns a timeout decorator that will raise an exception if the function takes longer than the specified timeout
def deadline(timeout):
    def decorate(f):
        def new_f(*args, **kwargs):
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(f, *args, **kwargs)
                return future.result(timeout=timeout)
        new_f.__name__ = f.__name__
        return new_f
    return decorate

# This function tests if the URL is accessible
@deadline(10)
def is_URL_accessible(url):
    # Create a list of user agents to be used for making requests in order to avoid being blocked
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]

    page = None
    try:
        headers = {'User-Agent': random.choice(user_agents)}
        page = requests.get(url, headers = headers, timeout=5)
    except requests.exceptions.RequestException:
        return False
    except concurrent.futures.TimeoutError:
        return False

    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
        return True
    else:
        return False

raw_dataset_filepath = 'datasets/raw_dataset.csv'
raw_dataset = dp.load_data(raw_dataset_filepath)
accessibility_df = pd.DataFrame(columns=['url', 'accessible', 'status'])

# Loop through the last 100 links in the raw dataset's URLs and test if they are accessible
for index, row in raw_dataset.tail(100).iterrows():
    print("Checking URL: " + row['url'])

    url = row['url']
    try:
        accessible = is_URL_accessible(url)
    except:
        accessible = False
    status = row['status']

    df = pd.DataFrame(columns=['url', 'accessible', 'status'], data=[[url, accessible, status]])
    accessibility_df = pd.concat([accessibility_df, df])

# Save the accessibility DataFrame to a CSV
accessibility_df.to_csv('datasets/raw_dataset_website_accessibility.csv', index=False)

print("\nEnd of program.")