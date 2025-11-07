# 📰 News Article Crawling for North Korea Provocation Detection  
**(뉴스기사 크롤링을 통한 북한 도발 징후 포착)**  

_Developed by Team “일등이조” as part of the Hanwha Aerospace Smart Defense Data Analysis Bootcamp (2025)_

---

## 📘 Overview  

Since the Korean Armistice Agreement in 1953, North Korea has repeatedly conducted provocations—often preceded by subtle political or media signals.  
This project aims to **detect early signs of such provocations** by crawling and analyzing news articles from **North Korea (KCNA)** and **South Korea (Kookbang Daily)**,  
as well as from major neighboring countries (**U.S., China, and Russia**).  

All data were collected, cleaned, analyzed, and visualized through an **interactive Streamlit dashboard** that provides insight into the temporal and political patterns of provocations.  

> Inspired by *Heinrich’s Law* — “For every major incident, there are hundreds of warning signs.”

---

## 🎯 Objectives  

- Detect early signs of North Korean provocations using large-scale news data  
- Collect and analyze **articles from 1 month before 14 major provocation events**  
- Compare with a **6-month “peace period”** to identify changes in tone and frequency  
- Classify and visualize provocations by **type** and **political regime**  
- Develop a **data-driven interactive dashboard** for defense and security research  

---

## 👥 Team Members  

| Name | Role | Responsibilities |
|------|------|------------------|
| **Kim Youngseong** | Data Collection / Analysis | South Korean articles, balloon incident data, provocation-type analysis |
| **Kim Jimin** | Data Collection / Visualization | Missile & KCNA data collection, preprocessing, word cloud and map visualization |
| **Shin Kyeongmin** | Database / Dashboard Development | DB creation, main/attack/nuclear pages, stacked & ratio charts |
| **Hyun Jiyeong** | Data Analysis / Presentation | Nuclear test data, news volume analysis, dashboard design, final presentation |

---

## 🗂️ Project Structure  
```bash
NK-Provocation-Detection/
│
├── 01_data/ # Cleaned and processed datasets
│ ├── attack.csv
│ ├── balloon.csv
│ ├── missile.csv
│ ├── nuclear.csv
│ └── provocation.csv
│
├── 02_notebooks/ # Jupyter notebooks for ETL and analysis
│ ├── 01_crawling/ # News crawling scripts
│ │ ├── kr_articles_crawl_by_country.ipynb
│ │ ├── kr_articles_crawl_preprocess_all.ipynb
│ │ └── nk_articles_crawl_by_country_all.ipynb
│ │
│ ├── 02_preprocessing/ # Data cleaning and merging
│ │ ├── nk_kr_articles_preprocessing.ipynb
│ │ └── provocation_data_clean_merge.ipynb
│ │
│ └── 03_analysis/ # Exploratory and visualization analyses
│ ├── generate_wordclouds.ipynb
│ ├── keyword_frequency_comparison.ipynb
│ ├── news_volume_timeline_analysis.ipynb
│ └── provocation_type_regime_analysis.ipynb
│
├── 03_streamlit_app/ # Streamlit dashboard application
│ ├── images/ # Word cloud and visualization assets
│ ├── pages/ # Sub-pages (Attack, Missile, Nuclear, Balloon)
│ ├── utils/ # Helper functions (preprocessing, charts, etc.)
│ ├── main.py # Main dashboard script
│ ├── README.md
│ └── requirements.txt
│
├── 04_docs/ # Documentation
│ ├── project_proposal/ # Project proposal document
│ ├── references/ # Data sources and bibliographic references
│ └── mysql_setup.md # MySQL setup and connection guide
│
├── 05_presentation/ # Final presentation materials
│ └── nk_provocation_detection_presentation.pdf
│
└── README.md # (This document)
```
---

## ⚙️ How to Run  

### 1️⃣ Install dependencies  
```bash
cd dashboard
pip install -r requirements.txt
```

### Set up MySQL
Refer to `docs/mysql_setup.md` and modify the database credentials in `main.py`:
```python
username = 'first'
password = '1emddlwh'
db_name = 'att_db'
host = 'localhost'
```
### 3️⃣ Launch the Streamlit dashboard
```bash
streamlit run main.py
```

## 📊 Dashboard Features

| Page | Description |
|------|-------------|
| **Main Page** | Folium map of provocation locations, regime-based charts, event ratio donut chart |
| **Attack Page** | Visualizes infiltration and naval attack events (e.g., Yeonpyeong, Cheonan) |
| **Missile Page** | Missile launches with pre-event word clouds and trend charts |
| **Nuclear Page** | Nuclear test event timelines and keyword comparison |
| **Balloon Page** | Garbage balloon incidents and article-based keyword patterns |

---

## 🧩 Data Description

| Dataset | Description | Source |
|----------|--------------|--------|
| **Missile Provocations** | Missile launches and test events | NTI (CNS North Korea Missile Test Database) |
| **Nuclear Tests** | Yearly nuclear test data | Wikipedia, Beyond Parallel |
| **Balloon Incidents** | Garbage balloon attacks | Beyond Parallel (CSIS) |
| **Infiltration / Attack** | Yeonpyeong, Cheonan, DMZ incidents | National Assembly Library, NIS |
| **News Articles** | North (KCNA) and South (Kookbang Daily) articles | [KCNA Watch](https://kcnawatch.org), [Kookbang Daily](https://kookbang.dema.mil.kr) |

> Total of **~130,000 news articles** collected and processed.

---

## 🧹 Data Preprocessing Steps

- Standardized date format (`YYYY-MM-DD`)
- Added regime columns: `n_gov` (North Korea) and `s_gov` (South Korea)
- Removed noise, special characters, and stopwords
- Conducted morphological analysis using **KoNLPy**
- Split datasets by **provocation period** and **peace period** for comparison

---

## 📈 Key Analyses

- **Provocation Type Distribution** — Frequency by missile, nuclear, attack, balloon  
- **Regime-based Comparison** — Patterns across different North/South Korean regimes  
- **Article Volume Change** — Trends in article counts before provocations  
- **Keyword & Wordcloud Analysis** — Frequent words during pre-provocation periods  
- **Geospatial Visualization** — Event locations with interactive markers  

---

## 💻 Tech Stack

| Category | Tools / Libraries |
|-----------|------------------|
| **Data Crawling** | `Selenium`, `BeautifulSoup`, `requests` |
| **Data Processing** | `pandas`, `numpy`, `konlpy`, `re`, `wordcloud` |
| **Visualization** | `matplotlib`, `seaborn`, `folium` |
| **Web Dashboard** | `Streamlit`, `MySQL`, `SQLAlchemy` |

---

## 🌱 Expected Impact

- Enable **early detection** of North Korean provocation signals  
- Support for **national defense and policy analysis** through open data  
- Foundation for expanding into **cyber or hybrid provocation detection models**

---

## 📚 References

- Kim, Donghoon (2021). *Catching Signs of Provocation of North Korea Using BERT-Based Language Modeling.* Seoul National University, Master’s Thesis  
- NTI (CNS North Korea Missile Test Database)  
- Beyond Parallel (CSIS) — *North Korean Provocations Database*  
- Wikipedia — *List of North Korean Nuclear Tests*  
- Kookbang Daily, KCNA Watch  

---

## 🧾 Additional Documents

- `dashboard/README.md` → Detailed instructions for running and navigating the dashboard  
- `docs/project_proposal/` → Original Korean project plan  
- `notebooks/` → Full analysis workflow from data collection to visualization

© 2025 Team 1등이조 | Hanwha Aerospace Smart Defense Data Analysis Bootcamp