# 📊 Data Description

This folder contains the raw and processed datasets used in the **North Korea Provocation Dashboard Project**.

---

## 1️⃣ Dataset Overview

| Category | Dataset Name | File Size | Records | Format | Source |
|-----------|---------------|-----------|----------|---------|---------|
| **Provocation Types** | Attack | 17KB | 252 | `.xlsx` | National Intelligence Service, National Assembly Library |
|  | Nuclear Tests | 2KB | 6 | `.csv` | Beyond Parallel, Wikipedia |
|  | Missile Provocations | 213KB | 309 | `.xlsx` | NTI (Nuclear Threat Initiative) |
|  | Balloon Attacks | 31KB | 168 | `.csv` | Beyond Parallel |
| **South Korean Articles (Full)** | Battle of Yeonpyeong II | 1200KB | 620 | `.csv` | Korea Defense Daily |
|  | 1st–6th Nuclear Tests, Missile Launches, etc. | Various | ~15 Files | `.csv` | Korea Defense Daily |
| **South Korean Articles (By Country)** | Same 15 Events | Various | ~15 Files | `.csv` / `.xlsx` | Korea Defense Daily |
| **North Korean Articles (Full)** | Same 15 Events | Various | ~15 Files | `.csv` | KCNA (Korean Central News Agency) |
| **North Korean Articles (By Country)** | Same 15 Events | Various | ~15 Files | `.csv` / `.xlsx` | KCNA |

---

## 2️⃣ Selected Key Provocation Events

The following 16 events were selected as major analysis targets based on government/military responses and media coverage.

| No. | Major North Korean Provocation | Date of Event | Analysis Period (Before Event) | Selection Rationale |
|-----|--------------------------------|----------------|-------------------------------|---------------------|
| 1 | 1st Battle of Yeonpyeong | 1999.06.15 | 1999.05.14–1999.06.14 | Government & military response; high media attention |
| 2 | 2nd Battle of Yeonpyeong | 2002.06.29 | 2002.05.28–2002.06.28 | Government response, casualties (6 KIA) |
| 3 | 1st Nuclear Test | 2006.10.09 | 2006.09.08–2006.10.08 | Strong international and domestic response |
| 4 | 2nd Nuclear Test | 2009.05.25 | 2009.04.24–2009.05.24 | Government & media focus (academic reference) |
| 5 | Cheonan Corvette Sinking | 2010.03.26 | 2010.02.25–2010.03.25 | Major military provocation; nationwide coverage |
| 6 | Yeonpyeong Island Shelling | 2010.11.23 | 2010.10.22–2010.11.22 | Direct military attack on civilians |
| 7 | 3rd Nuclear Test | 2013.02.12 | 2013.01.11–2013.02.11 | Repeated nuclear escalation |
| 8 | East Sea Short-Range Missile Launch | 2014.03.28 | 2014.02.27–2014.03.27 | Rapid increase in missile frequency from 2014 |
| 9 | DMZ Landmine Incident | 2015.08.04 | 2015.07.03–2015.08.03 | High-profile incident triggering military tension |
| 10 | 4th Nuclear Test | 2016.01.06 | 2015.12.05–2016.01.05 | Government & international response |
| 11 | 5th Nuclear Test | 2016.09.09 | 2016.08.08–2016.09.08 | Follow-up escalation from 4th test |
| 12 | 6th Nuclear Test | 2017.09.03 | 2017.08.02–2017.09.02 | Largest nuclear test to date |
| 13 | Series of Short-Range Missile Launches | 2019.05.09 | 2019.04.08–2019.05.08 | First provocation in 17 months |
| 14 | ICBM Launch South of NLL | 2022.11.02 | 2022.10.01–2022.11.01 | First missile south of NLL; ROK Air Force response |
| 15 | Waste Balloon Attacks | 2024.05.28 | 2024.04.28–2024.05.28 | New type of provocation (waste balloons) |
| 16 | Period with No Provocation (Control) | — | 2011.03.01–2011.09.30 | Comparative baseline period |

---

## 3️⃣ Notes

- All article datasets are collected from **Korea Defense Daily** and **KCNA**, and preprocessed for keyword and sentiment analysis.  
- Provocation data (type, date, source) were curated from multiple verified databases (NTI, Beyond Parallel, Wikipedia).  
- Each analysis period includes **1 month prior** to the provocation date to compare media trends.  

---

📚 **References**
- National Assembly Library Reports  
- NTI: [https://www.nti.org](https://www.nti.org)  
- Beyond Parallel: [https://beyondparallel.csis.org](https://beyondparallel.csis.org)  
- Wikipedia: North Korea Nuclear Tests  
- KCNA Watch: [https://kcnawatch.org](https://kcnawatch.org)
