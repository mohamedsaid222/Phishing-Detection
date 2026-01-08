# 🛡️ Phishing URL Detector (Advanced Machine Learning Project)

## 🌟 Project Overview
This project presents an end-to-end Machine Learning solution for the real-time detection of Phishing (malicious) URLs. We utilized a Random Forest Classifier trained on 13 specialized features extracted from URLs. The primary focus of this project was to achieve high accuracy while implementing a robust **Bias Mitigation Strategy** to ensure reliability on complex, legitimate links.

| Metric | Value |
| :--- | :--- |
| **Core Algorithm** | Random Forest Classifier |
| **Initial Accuracy** | ~91.57% |
| **Deployment Framework**| Streamlit |
| **Bias Mitigation** | Log Transformation on Length Features |

---

## 🧠 Model Architecture & Feature Engineering

The model relies on a fixed set of 13 features engineered to capture structural and lexical characteristics indicative of phishing attempts.

### 📊 Feature Set Used

The features are categorized into four types:

| Category | Feature Name | Description |
| :--- | :--- | :--- |
| **Length (Log-Scaled)** | `url_length` | Total length of the URL (Log(1+x)). |
| **Length (Log-Scaled)** | `path_length` | Length of the path component (Log(1+x)). |
| **Lexical/Symbolic** | `at_symbol` | Count of '@' symbols (often used in phishing). |
| **Lexical/Symbolic** | `nb_hyphens` | Count of '-' hyphens. |
| **Lexical/Symbolic** | `nb_underscore` | Count of '_' underscores. |
| **Lexical/Symbolic** | `nb_dots` | Count of '.' dots. |
| **Lexical/Symbolic** | `nb_and` | Count of '&' symbols. |
| **Content** | `sensitive_words_count` | Count of words like 'login', 'bank', 'secure', etc. |
| **Structural/Domain** | `nb_www` | Presence of 'www' (Binary). |
| **Structural/Domain** | `nb_com` | Count of '.com' occurrences. |
| **Structural/Domain** | `nb_or` | Presence of 'or' keyword (Binary). |
| **Structural/Domain** | `valid_url` | Always 1 (Placeholder for validation). |
| **Protocol** | `isHttps` | Uses HTTPS (1) or HTTP (0). |

---

## 💡 Bias Mitigation Strategy (Key Technical Detail)

### The Problem: Overfitting and False Positives
The initial Random Forest model was severely **biased** towards long URLs. Because legitimate, but complex, URLs (like Google Search results) are often very long, the model incorrectly classified them as Phishing with high confidence ($\sim 90\%$). This is a critical failure (high False Positive Rate). 

### The Solution: Log Transformation
To resolve this **Model Bias**, we implemented a standard pre-processing technique called **Log Transformation** ($\log(1+x)$) on the two main culprits: `url_length` and `path_length`.

1.  **Why Log Transformation?** It compresses the large scale of long lengths into a smaller, more manageable range. This reduces the feature's overpowering influence on the decision-making process.
2.  **Implementation:** The model was **re-trained** entirely on the dataset where the length features were replaced with their $\log(1+x)$ values.
3.  **Result:** The de-biased model now accurately classifies long, safe URLs (e.g., Google/LinkedIn) with **high Legitimate confidence ($\sim 99\%$)**, proving the success of the mitigation strategy.

---

## 🚀 Deployment and Local Setup

The project is deployed using Streamlit for an interactive web interface.

### 1. Repository Contents
Ensure you have the following files:
* `app.py`: The Streamlit application interface.
* `url_phishing_model_final_deployment.pkl`: The final, de-biased Random Forest model.
* `requirements.txt`: List of required Python packages.
* `README.md`: This file.

### 2. Setup and Installation

First, clone the repository:

```bash
git clone <YOUR-REPO-LINK>
cd Phishing-URL-Detector
