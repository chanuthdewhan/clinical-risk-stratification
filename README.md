# Strategic Patient Risk Stratification: Hospital Readmission Analytics

> A data-driven approach to reducing 30-day diabetic patient readmissions and mitigating HRRP financial penalties at Virtual Health Network (VHN)  

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

---

## 📋 Table of Contents

- [Executive Summary](#executive-summary)
- [Business Context](#business-context)
- [Key Findings](#key-findings)
- [Technology Stack](#technology-stack)
- [Project Methodology](#project-methodology)
- [Repository Structure](#repository-structure)
- [Installation & Usage](#installation--usage)
- [Results & Validation](#results--validation)
- [Recommendations](#recommendations)
- [Contributors](#contributors)
- [License](#license)

---

## 🎯 Executive Summary

Hospital readmissions within 30 days trigger significant Medicare penalties under the Hospital Readmissions Reduction Program (HRRP). This project analyzes **101,766 diabetic patient encounters** to identify clinical and operational risk factors driving preventable readmissions.

**Key Achievements:**

- ✅ Identified **11.47%** verified HRRP penalty cohort from initial 18% raw estimate
- ✅ Developed **Vitality Complexity Index (VCI)** with **1.8x risk lift** (17.1% vs 9.6% readmission rates)
- ✅ Discovered **54% readmission rate** for Home Health Services—highest operational failure point
- ✅ Built automated web scraping pipeline to enrich **top 20 ICD-9 diagnosis codes**
- ✅ Provided **3 actionable recommendations** for immediate operational deployment
- ✅ Delivered comprehensive 30-minute executive presentation

---

## 💼 Business Context

### The HRRP Challenge

The Centers for Medicare & Medicaid Services (CMS) penalizes hospitals with excessive readmissions by reducing up to **3% of ALL Medicare reimbursements**—not just for readmitted patients, but across the entire institution.

### The Problem

VHN's current discharge planning operates reactively:

- Decisions based on clinical intuition rather than data
- No systematic way to identify high-risk patients before discharge
- "One-size-fits-all" approach fails complex patients (insulin users, elderly, multiple comorbidities)

### Our Solution

A data-driven risk stratification system that flags high-risk patients **before discharge**, enabling targeted interventions where they matter most.

---

## 🔍 Key Findings

### 1. **The Insulin Risk Signal**

- Patients on insulin: **~49% readmission rate**
- Insulin = marker for disease severity + management complexity
- Current standardized discharge education is failing this cohort

### 2. **The Home Health Paradox**

- Home Health Services discharge: **54% long-term readmission rate** (13% within 30 days)
- **Higher than skilled nursing facilities**
- Over 54% of Home Health patients are insulin-dependent (compounding risk)

### 3. **The Geriatric Challenge**

- Peak patient volume: **70-80 years old**
- Discharge plans must account for vision loss, hearing decline, mobility issues
- Small-font instructions and complex apps will fail

### 4. **Duration ≠ Safety**

- Median length of stay: **~4 days** (identical for readmitted vs. safe patients)
- Keeping patients longer doesn't reduce readmission risk
- Risk driven by disease complexity, not bed days

### 5. **Demographic Disparities**

- 30-day penalty rates nearly identical across demographics (~11.5%)
- Driven by **social determinants**: transportation, medication costs, food security
- Not biological differences

---

## 🛠️ Technology Stack

### Core Technologies

```
Python 3.8+
├── Data Processing
│   ├── pandas (data manipulation)
│   ├── numpy (numerical operations)
│   └── datetime (temporal analysis)
├── Visualization
│   ├── matplotlib (plotting)
│   └── seaborn (statistical graphics)
└── Web Scraping
    ├── requests (HTTP requests)
    └── BeautifulSoup4 (HTML parsing)
```

### Development Environment

- **IDE:** Jupyter Notebook / VS Code (Jupyter extension)
- **Version Control:** Git

---

## 📊 Project Methodology

### Phase 1: Data Cleaning & Preprocessing

**Challenge:** Raw hospital data with 101,766 encounters required rigorous cleaning.

**Actions Taken:**

1. **Data Type Correction**
   - Identified categorical IDs stored as integers (`admission_type_id`, `discharge_disposition_id`, `admission_source_id`)
   - Converted to strings to prevent algorithms treating them as continuous numerical features

2. **Missing Data Strategy**
   - Dropped `weight` column (96.8% missing, exceeded 90% threshold)
   - Dropped `payer_code` (~40% missing, low clinical relevance)
   - Retained `medical_specialty`, recoded `?` as `"Missing"` to preserve structure
   - Remaining nulls in race/diagnosis handled via row deletion

3. **Deceased Patient Exclusion**
   - Removed **1,616 patients** who expired (discharge codes 11, 19, 20, 21)
   - **Critical:** Deceased patients cannot be readmitted—inclusion would artificially inflate success rates

4. **Duplicate Check**
   - Verified no duplicate records found

**Result:** Clean analytical dataset of **96,437 records**

---

### Phase 2: Exploratory Data Analysis (EDA)

**Objective:** Understand demographic patterns, clinical drivers, and operational inefficiencies.

#### 2.1 Readmission Landscape

- **Class Imbalance:** 11.47% (<30 days) vs. 88.53% (safe)
- Challenge: Can't just predict "no readmission" (89% accuracy but clinically useless)

#### 2.2 Demographic Analysis

- Age distribution peaks at **70-80 years**
- Geriatric challenge requires age-appropriate interventions

#### 2.3 Clinical Metrics

- **Medication Analysis:**
  - Insulin users: ~49% readmission rate (highest risk cohort)
  - Medication changes during stay increase risk
- **Operational Metrics:**
  - Correlation heatmap confirmed low multicollinearity (max 0.46)
  - Scatter plot: Longer stays → more lab tests → higher costs
  - Box plot: Length of stay does NOT reduce readmission risk

#### 2.4 Discharge Disposition Failure

- Home Health Services: **54% long-term readmission** (13% <30 days)
- Unknown discharge destination: **42% return rate** (documentation failure)

---

### Phase 3: Web Scraping for Diagnostic Clarity

**Problem:** Dataset contained only ICD-9 numerical codes (e.g., "428", "250.8")—meaningless for analysis.

**Solution:** Automated web scraper to translate codes into human-readable disease descriptions.

#### Scraper Architecture

```python
def fetch_icd9_description(code):
    """
    Scrapes ICD-9 description from medical database
    - Handles code padding (38 → 038)
    - Implements 1-second delay (ethical scraping)
    - Returns clean description or "Description Not Found"
    """
```

**Key Features:**

- **Smart Padding:** Automatically pads numeric codes to 3 digits (e.g., `38` → `038`)
- **Error Handling:** Try/except blocks with 10-second timeout for graceful failure
- **Ethical Design:** 1-second delay between requests (mimics human behavior, prevents server overload)
- **HTML Parsing:** BeautifulSoup extracts description from target div class

**Target:** Top 20 most frequent diagnosis codes

**Results:**

```
Code 428  → Heart failure
Code 38   → Septicemia
Code 486  → Pneumonia, organism unspecified
Code 250.8 → Diabetes with other specified manifestations
Code 584  → Acute renal failure
... (15 more)
```

**Impact:** Enabled meaningful comorbidity counting for VCI calculation

---

### Phase 4: Vitality Complexity Index (VCI)

**Objective:** Create transparent, nurse-friendly risk score (not a "black box" machine learning model).

**Methodology:** Adapted industry-standard LACE index for VHN's data.

#### VCI Components

| Component                 | Description                                    | Weight Logic                                             |
| ------------------------- | ---------------------------------------------- | -------------------------------------------------------- |
| **L** - Length            | Duration of hospital stay                      | Extended stays (14+ days) signal complications           |
| **A** - Acuity            | Admission type (Emergency/Trauma vs. Elective) | Emergency arrivals indicate instability                  |
| **C** - Comorbidity       | Number of concurrent diagnoses                 | 8 conditions > 2 conditions (thanks to ICD-9 enrichment) |
| **E** - Emergency History | Past ER visits in 12 months                    | Past behavior predicts future patterns                   |

**Scoring:** VCI = L + A + C + E

---

## 📈 Results & Validation

### VCI Performance

Stratified patients into risk categories:

| Risk Level | VCI Score | Actual Readmission Rate | Interpretation                                      |
| ---------- | --------- | ----------------------- | --------------------------------------------------- |
| **Low**    | < 7       | 9.6%                    | Stable, standard discharge appropriate              |
| **Medium** | 7-10      | ~13%                    | Moderate risk, enhanced monitoring                  |
| **High**   | > 10      | 17.1%                   | **1.8x higher risk**, intensive intervention needed |

**Key Insight:** The model successfully identifies high-risk patients with **nearly double** the readmission rate of low-risk patients.

**Transparency Advantage:** Nurses can see exactly why a patient was flagged (e.g., "Emergency admission + 15-day stay + 6 diagnoses + 4 prior ER visits"), building trust and clinical buy-in.

---

## 💡 Strategic Recommendations

### 1. Deploy VCI as Digital Triage

**Action:** Integrate VCI score into EHR nursing dashboard

- Automatic "High Risk" alert when VCI > 10
- Enables proactive discharge planning from day 1 (not scrambling on discharge day)

**Impact:** Focus expensive case management resources on the 11.47% who drive penalties

---

### 2. Overhaul Home Health Safety Net

**Problem:** 54% readmission rate = broken system

**Actions:**

- **Mandate:** High-risk patients (VCI > 10) must have nursing visit within **24 hours** (not 48-72 hours)
- **Require:** Structured handoff call between VHN nurse and home health nurse before discharge
- **Ensure:** Clear communication about medications, warning signs, interventions

**Impact:** Close the gap where 54% of patients are currently falling through

---

### 3. Create Insulin Mastery Program

**Problem:** 49% readmission rate for insulin users with generic education

**Actions:**

- **Segregate:** Specialized discharge track for insulin-dependent patients
- **Implement:** Teach-back methodology (patients demonstrate injection technique)
- **Cover:** Hypoglycemia recognition, storage requirements, timing
- **Assess:** Home environment (refrigeration access, test strip affordability)

**Impact:** Address root cause of readmissions for highest-risk medication cohort

---

## 📁 Repository Structure

```
clinical-risk-stratification/
│
├── data/                                # Dataset files
│   ├── diabetic_data.csv                # Original dataset (101,766 records)
│   ├── IDs_mapping.csv                  # Categorical ID mappings
│   └── final_diabetes_analysis_VCI.csv  # Processed data with VCI scores
│
├── notebooks/                             # Jupyter notebooks
│   └── technical_appendix_modeling.ipynb  # Complete analysis pipeline
│
├── graph/                              # Generated visualizations
│   └── [All EDA and analysis plots]
│
├── reports/                            # Project deliverables
│   ├── Strategic_Insight_Report.pdf    # Business Report
│   └── VHN_Readmission_Presentation    # Executive Presentation
│
└── README.md                           # This file
```

---

## 🚀 Installation & Usage

### Prerequisites

```bash
Python 3.8 or higher
pip package manager
```

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/chanuthdewhan/clinical-risk-stratification.git
cd clinical-risk-stratification
```

2. **Create virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install pandas numpy matplotlib seaborn requests beautifulsoup4 jupyter
```

4. **Launch Jupyter Notebook**

```bash
jupyter notebook
```

5. **Open the analysis notebook**

- Navigate to `notebooks/technical_appendix_modeling.ipynb`
- Run cells sequentially to reproduce the analysis

### Required Libraries

```txt
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
requests>=2.26.0
beautifulsoup4>=4.9.0
jupyter>=1.0.0
```

---

## 📊 Sample Code Snippets

### VCI Calculation

```python
def calculate_L_score(days):
    """ L - Length of Stay Score """
    if days < 1:
        return 0
    elif 1 <= days <= 4:
        return 1
    elif 5 <= days <= 13:
        return 4
    else:
        return 7  # >= 14 days

def calculate_A_score(admission_id):
    """ A - Acuity of Admission Score (1=Emergency, 7=Trauma) """
    if admission_id in [1, 7]:
        return 3
    else:
        return 0

def calculate_C_score(num_diagnoses):
    """ C - Comorbidity Burden Score (Proxy: Count of Diagnoses) """
    if num_diagnoses < 4:
        return 0
    elif 4 <= num_diagnoses <= 7:
        return 3
    else:
        return 5  # >= 8 diagnoses

def calculate_E_score(num_visits):
    """ E - Emergency Visit Intensity Score """
    if num_visits == 0:
        return 0
    elif 1 <= num_visits <= 4:
        return 3
    else:
        return 5  # >4 visits
```

### Web Scraper Example

```python
def fetch_icd9_description(code):
    """
    Scrapes the ICD-9 description for a given code.
    - Handles padding (38 -> 038).
    - Extract returns the target desc.
    """
    BASE_URL = "http://icd9.chrisendres.com/index.php"

    # Pad numeric codes to 3 digits (Website requirement)
    search_term = code.zfill(3) if len(code) < 3 and not code.startswith(('V', 'E')) else code

    params = {
        'action': 'search',
        'srchtext': search_term,
        'srchtype': 'diseases',
        'Submit': 'Search'
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract content from target div-'dlvl'
        desc_div = soup.find('div', class_='dlvl')

        if desc_div:
            full_text = desc_div.get_text(strip=True)

            # Remove the search term(code) from the result to get only desc.
            clean_desc = full_text.replace(str(search_term), '', 1).strip()
            return clean_desc

        return "Description Not Found"

    except Exception as e:
        print(f"Error scraping {code}: {e}")
        return "Description Not Found"


# Usage with ethical delay
for code in target_codes:
    description = fetch_icd9_description(code)
    icd_descriptions[code] = description
    print(f"Code {code}: {description}")

    # 1-second delay between requests
    time.sleep(1)
```

---

## 🎓 Key Learnings

### Technical

- **Class imbalance handling:** Can't optimize for accuracy when target is 11%—must focus on precision/recall
- **Clinical data requires clinical logic:** Not all missing values should be imputed
- **Transparency matters:** Explainable models (VCI) build trust vs. black-box ML

### Business

- **Operational failures > clinical failures:** Home Health paradox shows system issues
- **Duration ≠ quality:** Keeping patients longer wastes money without improving outcomes
- **Targeted interventions:** Insulin users need specialized care, not generic education

---

## 🎤 Presentation

An interactive **30-minute presentation** was delivered to the VHN Executive Board covering:

- Business context and HRRP financial implications
- Data methodology and cleaning process
- Key findings and operational failures
- VCI model validation
- Strategic recommendations

**Format:** HTML slideshow (navigate with arrow keys)  
**Location:** `reports/presentation_slides.html`  
**Duration:** 30 minutes (5 presenters, 4 phases)

**To view:** Open `presentation_slides.html` in any web browser

## 👥 Contributors

**Project Team:**

- Praveen Rusiru [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/praveen-rusiru) [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/PraveenRusiru)
- Ruwani Ranthika [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/ruwani-ranthika-ba4186314) [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/ruwani425)
- Dinan Themika [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/dinan-themika-651bab289) [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/DTY17)
- Chanuth Dewhan [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/chanuthdewhan) [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/chanuthdewhan)

**Academic Context:**

- GDSE 72
- Institution: IJSE - Institute of Software Engineering
- Lecturer: Mr. Dasun Athukorala

---

## 🙏 Acknowledgments

- Virtual Health Network for the business case
- UCI Machine Learning Repository for the diabetes dataset
- ICD-9 database for diagnostic code mappings
- Our academic supervisor for guidance and feedback

---

<p align="center">
  <strong>Built with 🩺 for better patient outcomes</strong>
</p>
