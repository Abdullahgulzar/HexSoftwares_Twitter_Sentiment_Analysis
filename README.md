# HexSoftwares_Twitter_Sentiment_Analysis

# 🐦 Twitter Sentiment Analysis using NLP

An AI-powered **Twitter Sentiment Analysis** application built using **TextBlob NLP** as part of the **Hex Softwares AI Internship Program (Task 3)**. The app analyzes tweets and classifies them as Positive, Negative, or Neutral — with a fully interactive dark-themed GUI and live statistics dashboard.

---

## 🤖 What is this Project?

**SentimentAI** is a desktop application that uses Natural Language Processing (NLP) to analyze the sentiment of tweets or any text input — deployed as a complete GUI application with real-time stats, CSV import/export, and a modern dark-themed interface built in Python.

---

## 💬 Features

- ✍️ **Text Input** — Type or paste any tweet/text for instant sentiment analysis
- 📋 **Sample Tweets** — 15 pre-loaded demo tweets analyzed in one click
- 📁 **CSV Import** — Import real Twitter datasets (Kaggle/custom CSV files)
- 😊😞😐 **Result Card** — Big emoji + color-coded label + polarity score
- 📊 **Live Statistics** — Real-time Positive / Negative / Neutral counter
- 📜 **History Table** — All analyzed tweets stored in a color-coded table
- 💾 **Export CSV** — Save all results with sentiment scores to CSV
- 🌙 **Dark Mode GUI** — Modern dark-themed desktop interface
- ⚡ **Threading** — Background CSV processing, GUI never freezes

---

## 🛠️ Technologies Used

- Python 3.8+
- TextBlob — NLP Sentiment Analysis
- Tkinter — GUI Framework
- CSV / Pandas — Data handling
- Threading — Background processing

---

## 🔄 How it Works

```
Input (Text / Tweet / CSV)
        ↓
TextBlob NLP Processing
        ↓
Polarity Score calculated (-1.0 to +1.0)
        ↓
Classified as POSITIVE / NEGATIVE / NEUTRAL
        ↓
Result displayed with emoji + color + score
        ↓
Added to History Table + Live Stats updated
```

---

## 📊 Sentiment Scale

| Polarity Score | Label | Emoji |
|---|---|---|
| > +0.05 | POSITIVE | 😊 |
| < -0.05 | NEGATIVE | 😞 |
| -0.05 to +0.05 | NEUTRAL | 😐 |

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/Abdullahgulzar/HexSoftwares_Twitter_Sentiment_Analysis.git
cd HexSoftwares_Twitter_Sentiment_Analysis
```

**2. Install required libraries**
```bash
pip install textblob pandas
```

**3. Run the application**
```bash
python sentiment_analysis_gui.py
```

---

## 📁 CSV Import Guide

The app auto-detects common tweet columns: `content`, `text`, `tweet`, `body`

Recommended free datasets from Kaggle:
- Twitter US Airline Sentiment
- Sentiment140 Dataset
- Any CSV with a `text` or `content` column

---

## 🏢 Internship Details

| Detail | Info |
|---|---|
| **Company** | HexSoftwares |
| **Program** | AI Internship |
| **Task** | Task 3 — Twitter Sentiment Analysis |
| **Domain** | Artificial Intelligence / NLP |
| **Intern** | Shaikh Abdullah Siddique |



