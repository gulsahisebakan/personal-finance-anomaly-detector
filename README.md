# 💰 Personal Finance Anomaly Detector

> An end-to-end data analytics project that uses Machine Learning to automatically detect unusual spending patterns in personal finance data — built with Python, Scikit-learn, and Plotly Dash.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Dash](https://img.shields.io/badge/Dash-v4.0-teal?logo=plotly)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.8-orange?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

This project simulates a real-world financial analytics pipeline. It ingests a year's worth of bank transaction data, applies the **Isolation Forest** unsupervised machine learning algorithm to identify anomalous transactions, and presents the findings in a fully interactive dashboard.

This mirrors the kind of work done by data analysts at banks, fintech companies, and financial planning platforms every day.

---

## 🚀 Live Demo

Run locally and open your browser at `http://127.0.0.1:8050`

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Live%20on%20localhost-brightgreen)

---

## 🧠 How It Works

The project has three stages, each in its own Python file:

### 1. `generate_data.py` — Data Generation
- Generates 12 months of realistic bank transactions across 8 spending categories
- Injects 10 real anomalies (e.g. Christmas shopping, emergency healthcare, flight bookings)
- Saves output to `transactions.csv`

### 2. `detect_anomalies.py` — ML Anomaly Detection
- Loads transaction data using **Pandas**
- Engineers two features: raw transaction amount and **Z-score** (statistical deviation from category average)
- Trains an **Isolation Forest** model — an unsupervised ML algorithm that isolates outliers by asking *"how easy is it to separate this point from all others?"*
- Flags anomalies and saves full results to `transactions_analyzed.csv`

### 3. `dashboard.py` — Interactive Dashboard
- Builds a dark-themed interactive dashboard using **Plotly Dash**
- Displays summary KPI cards (total transactions, anomalies found, total spend, anomaly spend)
- Interactive scatter plot with all transactions — anomalies highlighted as red X markers
- Horizontal bar chart showing spend breakdown by category
- Monthly spending trend line chart
- Full anomaly table with Z-scores
- **Live category filter** that updates all charts simultaneously

---

## 📊 Key Findings (Sample Output)

| Date | Category | Amount | Note | Z-Score |
|------|----------|--------|------|---------|
| 2024-12-25 | Shopping | $2,000.00 | Christmas gifts | 7.41 |
| 2024-11-29 | Shopping | $1,500.00 | Black Friday | 5.39 |
| 2024-06-01 | Transport | $900.00 | Flight booking | 10.52 |
| 2024-08-15 | Healthcare | $750.00 | Emergency visit | 10.21 |
| 2024-05-10 | Entertainment | $650.00 | Concert tickets | 10.57 |

> The model successfully detected all 10 planted anomalies plus 8 additional statistically unusual transactions — demonstrating the power of unsupervised learning on real-world financial data.

---

## 🛠️ Technology Stack

| Tool | Purpose |
|------|---------|
| **Python 3.14** | Core programming language |
| **Pandas** | Data loading, cleaning, and transformation |
| **Scikit-learn** | Isolation Forest anomaly detection algorithm |
| **Plotly** | Interactive chart generation |
| **Dash** | Web dashboard framework |
| **NumPy** | Numerical computations and Z-score calculation |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/gulsahisebakan/personal-finance-anomaly-detector.git
cd personal-finance-anomaly-detector

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data
python generate_data.py

# 5. Run anomaly detection
python detect_anomalies.py

# 6. Launch the dashboard
python dashboard.py
```

Then open your browser and navigate to **http://127.0.0.1:8050**

---

## 📁 Project Structure

```
personal-finance-anomaly-detector/
│
├── generate_data.py          # Generates synthetic transaction data
├── detect_anomalies.py       # ML anomaly detection pipeline
├── dashboard.py              # Interactive Plotly Dash dashboard
├── transactions.csv          # Generated raw transaction data
├── transactions_analyzed.csv # Analyzed data with anomaly flags
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 💡 What I Learned

- Building an **end-to-end data pipeline** from raw data to visual insight
- Applying **unsupervised machine learning** (Isolation Forest) to a real-world problem
- **Feature engineering** — transforming raw amounts into meaningful statistical features (Z-scores)
- Creating **interactive dashboards** with callbacks and dynamic filtering
- Professional Python project structure with virtual environments

---

## 🔮 Future Improvements

- [ ] Connect to a real bank API (e.g. Plaid) to use actual transaction data
- [ ] Add email/SMS alerts when a new anomaly is detected
- [ ] Implement a budget forecasting module using time series analysis
- [ ] Add user authentication so multiple users can track their own finances
- [ ] Deploy to a cloud platform (Heroku, Railway, or AWS)

---

## 📄 License

MIT License — feel free to use, modify, and distribute this project.
