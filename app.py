import streamlit as st
import re
from urllib.parse import urlparse
import pandas as pd
import joblib
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🚨",
    layout="centered"
)

# --- MODEL AND THRESHOLD CONFIGURATION ---

# Standard threshold used after successful model debiasing
PHISHING_THRESHOLD = 0.50 
MODEL_PATH = 'url_phishing_model_final_deployment.pkl'

# The 13 required features
REQUIRED_FEATURES_FINAL = [
    'url_length', 'valid_url', 'at_symbol', 'sensitive_words_count', 'path_length', 
    'isHttps', 'nb_dots', 'nb_hyphens', 'nb_and', 'nb_or', 
    'nb_www', 'nb_com', 'nb_underscore'
]

# Feature Extraction Function (Matches the Log-Scaled training data)
def extract_features_final(url):
    """
    Extracts the 13 required features, applying Log Transformation 
    to length features to match the improved model's training set.
    """
    parsed_url = urlparse(url)
    features_dict = {feature: 0 for feature in REQUIRED_FEATURES_FINAL}

    # Raw length calculations
    raw_url_length = len(url)
    raw_path_length = len(parsed_url.path)
    
    # Applying Log Transformation (Log(1+x)) to mitigate length bias
    if 'url_length' in features_dict: features_dict['url_length'] = np.log1p(raw_url_length)
    if 'path_length' in features_dict: features_dict['path_length'] = np.log1p(raw_path_length)
    
    # Other features
    if 'valid_url' in features_dict: features_dict['valid_url'] = 1 
    if 'at_symbol' in features_dict: features_dict['at_symbol'] = url.count('@')
    if 'sensitive_words_count' in features_dict: features_dict['sensitive_words_count'] = len(re.findall(r'(login|bank|secure|verify|account|paypal)', url.lower()))
    if 'isHttps' in features_dict: features_dict['isHttps'] = 1 if parsed_url.scheme == 'https' else 0
    if 'nb_dots' in features_dict: features_dict['nb_dots'] = url.count('.')
    if 'nb_hyphens' in features_dict: features_dict['nb_hyphens'] = url.count('-')
    if 'nb_and' in features_dict: features_dict['nb_and'] = url.count('&') 
    if 'nb_or' in features_dict: features_dict['nb_or'] = 1 if 'or' in url.lower() else 0
    if 'nb_www' in features_dict: features_dict['nb_www'] = 1 if 'www' in parsed_url.netloc.lower() else 0
    if 'nb_com' in features_dict: features_dict['nb_com'] = url.lower().count('.com')
    if 'nb_underscore' in features_dict: features_dict['nb_underscore'] = url.count('_')
    
    features_df = pd.DataFrame([features_dict], columns=REQUIRED_FEATURES_FINAL)
    return features_df

# Model Loading Function
@st.cache_resource
def load_model():
    """Loads and caches the model file."""
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        st.error(f"Error: Model file '{MODEL_PATH}' not found. Please ensure it is in the same folder.")
        return None

def predict_url_final(url, model):
    """Predicts URL type using the de-biased feature set."""
    if not model:
        return "Error", 0, None
        
    features_df = extract_features_final(url)
    features_df = features_df.astype(float)
    
    # Prediction probabilities
    probabilities = model.predict_proba(features_df)[0]
    phishing_prob = probabilities[1]
    
    # Decision based on the standard 0.50 threshold
    if phishing_prob >= PHISHING_THRESHOLD:
        result = "Phishing"
        conf_score = phishing_prob * 100
    else:
        result = "Legitimate"
        conf_score = probabilities[0] * 100 
        
    return result, conf_score, features_df.T

# --- STREAMLIT UI ---


st.title("🛡️ URL Safety Check")
st.markdown("### Powered by Random Forest and Log Transformation")

user_url = st.text_input(
    "Enter a URL to check:",
    placeholder="e.g., https://www.google.com/search?q=...",
    key="url_input"
)

model = load_model()

if user_url and model:
    prediction, confidence, features_df = predict_url_final(user_url, model)
    
    if prediction == "Phishing":
        st.error(f"## 🚨 Result: **PHISHING**")
        st.markdown(f"#### Confidence Score: **{confidence:.2f}%**")
        st.warning("⚠️ Warning: This URL exhibits high malicious patterns.")
    else:
        st.success(f"## ✅ Result: **LEGITIMATE**")
        st.markdown(f"#### Confidence Score: **{confidence:.2f}%**")
        st.info("SAFE: The de-biased model confirms this URL is safe.")
        
    
