#  Pro Kabaddi League (PKL) Analysis Dashboard

A data-driven Streamlit web app analyzing **10 seasons of the Pro Kabaddi League (PKL)** — featuring player stats, team performance, match-level insights, and card analysis.  
Built with Python, Pandas, Plotly, and Streamlit.

---

## 📊 Key Features

-  **Season-Wise Match Insights** – Explore total points, wins, losses, and high-scoring matches by season.  
-  **Player-Level Stats** – Check player performances, raiders, and card records.  
-  **Team-Level Analysis** – Compare teams across seasons with visual charts.  
-  **Card Analysis** – View total Green, Yellow, and Red card distributions and top card receivers.  
-  **Interactive Player Lookup** – Search any player to instantly see their card summary.

---
## App Overview
![Dashboard Home](https://raw.githubusercontent.com/hemant-pm/images_/refs/heads/main/pkl_screenshots/pkl_1.png?token=GHSAT0AAAAAADLXNIXSYBNIGHLPFY5IYUMC2H4373Q)

![Matches Analysis](https://raw.githubusercontent.com/hemant-pm/images_/refs/heads/main/pkl_screenshots/pkl_2.png?token=GHSAT0AAAAAADLXNIXTRBKJYNRN4X4NU2LQ2H44BDA)

![Team Analysis](https://raw.githubusercontent.com/hemant-pm/images_/refs/heads/main/pkl_screenshots/pkl_3.png?token=GHSAT0AAAAAADLXNIXS37WZCWMH2JTZP4WA2H44BTA)

![Venue Insights](https://raw.githubusercontent.com/hemant-pm/images_/refs/heads/main/pkl_screenshots/pkl_4.png?token=GHSAT0AAAAAADLXNIXTMXEUQVROLXJLVPBC2H44CTQ)

![Player Analysis](https://raw.githubusercontent.com/hemant-pm/images_/refs/heads/main/pkl_screenshots/pkl_5.png?token=GHSAT0AAAAAADLXNIXSSP64B3TX5LT44SH22H44DLQ)
---
## [click here](https://pkl-analysis-season-1-10.streamlit.app/) to view interactive app.
---
## 📊 Data Collection Process

This project uses datasets collected from the Pro Kabaddi League (PKL) using the open-source Python library kabaddiPy.
- Two main datasets were created:
 - PKL_Rosters_Seasons_1-10.csv – Contains team rosters (players, teams, and season details).
 - PKL_All_Seasons_Matches.csv – Contains match-level data (teams, scores, venues, and dates).

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Visualization | Plotly Express |
| Language | Python 3.11+ |
| Data Processing | Pandas |

---

##  Run Locally
#### 1️ Clone the repository
```bash
git clone https://github.com/hemant-pm/PKL_Analysis.git
```
#### 2 Navigate to directory
```bash
cd PKL_Analysis
```
#### 3. Create virtual environment(Windows)
```bash
python -m venv pkl_venv
```
#### 4. Activate virtual environmet
```bash
pkl_venv\Scripts\activate
```
#### 5 Install dependencies
```bash
pip install -r requirements.txt
```
#### 6 Run Streamlit app
```bash
streamlit run streamlit_app.py
```
---
##### Hemant Mahajan
###### connect on - [Linkedin](https://www.linkedin.com/in/hemant-mahajan-3648642a0/)
###### Email - hemantmahajan1611@gmail.com
