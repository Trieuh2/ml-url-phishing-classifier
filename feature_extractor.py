import concurrent.futures
import content_features as confe
import numpy as np
import pandas as pd
import random
import re
import requests
import tldextract
import url_features as urlfe
import urllib.parse

from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function that extracts the hostname, domain, and path of the URL provided
def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path

# Function that performs both structural and statistical feature extractions on the provided URL and returns a combined vector
def extract_features(url, selected_structural_features, selected_statistical_features):
    structural_feature_vector = generate_structural_feature_vector(url, selected_structural_features)
    statistical_feature_vector = generate_statistical_feature_vector(url, selected_statistical_features)

    combined_vector = pd.concat([structural_feature_vector, statistical_feature_vector], axis = 1)
    return combined_vector

# Helper function that extracts the structural features of the URL
def extract_structural_features(url, scheme, domain, subdomain, extracted_domain, tld, path):
    row = [
        urlfe.having_ip_address(url),
        urlfe.https_token(scheme),
        urlfe.punycode(url),
        urlfe.port(url),
        urlfe.tld_in_path(tld, path),
        urlfe.tld_in_subdomain(tld, subdomain),
        urlfe.abnormal_subdomain(url),
        urlfe.prefix_suffix(url),
        urlfe.shortening_service(url),
        urlfe.domain_in_brand(extracted_domain.domain),
        urlfe.brand_in_path(extracted_domain.domain,subdomain),
        urlfe.brand_in_path(extracted_domain.domain,path),
        urlfe.suspicious_tld(tld),
        urlfe.statistical_report(url, domain),               
    ]
    return row

# Helper function that extracts the statistical features of the URL
def extract_statistical_features(url, hostname, path, words_raw, words_raw_host, words_raw_path):
    row = [
        urlfe.url_length(url),
        urlfe.url_length(hostname),
        urlfe.count_dots(url),
        urlfe.count_hyphens(url),
        urlfe.count_at(url),
        urlfe.count_questionmark(url),
        urlfe.count_and(url),
        urlfe.count_or(url),
        urlfe.count_equal(url),
        urlfe.count_underscore(url),
        urlfe.count_tilde(url),
        urlfe.count_percentage(url),
        urlfe.count_slash(url),
        urlfe.count_star(url),
        urlfe.count_colon(url),
        urlfe.count_comma(url),
        urlfe.count_semicolon(url),
        urlfe.count_dollar(url),
        urlfe.count_space(url),            
        urlfe.check_www(words_raw),
        urlfe.check_com(words_raw),
        urlfe.count_double_slash(url),
        urlfe.count_http_token(path),            
        urlfe.ratio_digits(url),
        urlfe.ratio_digits(hostname),
        urlfe.count_subdomain(url),          
        urlfe.length_word_raw(words_raw),
        urlfe.char_repeat(words_raw),
        urlfe.shortest_word_length(words_raw),
        urlfe.shortest_word_length(words_raw_host),
        urlfe.shortest_word_length(words_raw_path),
        urlfe.longest_word_length(words_raw),
        urlfe.longest_word_length(words_raw_host),
        urlfe.longest_word_length(words_raw_path),
        urlfe.average_word_length(words_raw),
        urlfe.average_word_length(words_raw_host),
        urlfe.average_word_length(words_raw_path),
        urlfe.phish_hints(url),  
    ]
    return row

# Function that performs data pre-processing, extracts the structural features of the URL and returns the results as a list
def generate_structural_feature_vector(url, selected_structural_features):
    hostname, domain, path = get_domain(url)
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    tld = extracted_domain.suffix
    parsed = urlparse(url)
    scheme = parsed.scheme
        
    res = extract_structural_features(url, scheme, domain, subdomain, extracted_domain, tld, path)
    all_structural_features = [
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
    df = pd.DataFrame([res], columns=all_structural_features)
    structural_feature_vector = df[selected_structural_features]
    
    return structural_feature_vector

# Function that processes the provided URL and returns a list of the statistical features of the URL
def generate_statistical_feature_vector(url, selected_statistical_features):
    def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())   
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None,raw_words))
        return raw_words, list(filter(None,w_host)), list(filter(None,w_path))

    hostname, domain, path = get_domain(url)
    extracted_domain = tldextract.extract(url)
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    words_raw, words_raw_host, words_raw_path= words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
    
    res = extract_statistical_features(url, hostname, path, words_raw, words_raw_host, words_raw_path)
    all_statistical_features = [
        'length_url',
        'length_hostname',
        'nb_dots',
        'nb_hyphens',
        'nb_at',
        'nb_qm',
        'nb_and',
        'nb_or',
        'nb_eq',
        'nb_underscore',
        'nb_tilde',
        'nb_percent',
        'nb_slash',
        'nb_star',
        'nb_colon',
        'nb_comma',
        'nb_semicolon',
        'nb_dollar',
        'nb_space',
        'nb_www',
        'nb_com',
        'nb_dslash',
        'http_in_path',
        'ratio_digits_url',
        'ratio_digits_host',
        'nb_subdomains',
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
    df = pd.DataFrame([res], columns=all_statistical_features)
    statistical_feature_vector = df[selected_statistical_features]
    return statistical_feature_vector