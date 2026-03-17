import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Hospital Readmission Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, clinical, enterprise look
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: left;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: left;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Modern floating metric cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #1f77b4;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #666666;
        font-weight: 600;
        font-size: 1rem;
    }

    [data-testid="stMetricValue"] {
        color: #1f77b4;
        font-weight: 700;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>VHN 🩺</h1>", unsafe_allow_html=True)
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["🌐 Overview", "📊 Data Insights", "🎯 VCI Model", "💡 Recommendations", "📁 About"]
    )
    
    st.divider()
    st.markdown("### Quick Stats")
    st.metric("Total Patients", "101,766")
    st.metric("Clean Dataset", "96,437")
    st.metric("Readmission Rate", "11.47%")

# Main content
if page == "🌐 Overview":
    st.markdown('<h1 class="main-header">🌐 Strategic Patient Risk Stratification</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Reducing Hospital Readmissions & Mitigating HRRP Penalties</p>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Patients Analyzed", value="101,766", delta="Raw encounters")
    with col2:
        st.metric(label="VCI", value="1.8x", delta="Prediction accuracy")
    with col3:
        st.metric(label="Home Health Failure", value="54%", delta="-13% vs SNF", delta_color="inverse")
    with col4:
        st.metric(label="Insulin Risk", value="49%", delta="Readmission rate", delta_color="inverse")
    
    st.divider()
    
    # Project overview
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📋 Project Overview")
        st.markdown("""
        Medicare's **Hospital Readmissions Reduction Program (HRRP)** penalizes hospitals with excessive readmissions 
        when patients with chronic diseases like diabetes return within 30 days.
        
        **The Challenge:**
        - Hospitals can lose up to **3% of ALL Medicare payments** across their entire revenue.
        - Without data-driven tools, hospitals cannot identify which patients need intensive support before discharge.
        
        **Our Solution:**
        We analyzed 100,000+ hospital encounters to predict which diabetic patients are most likely to be readmitted 
        within 30 days and identify the operational failures driving these readmissions.
        """)
    
    with col2:
        st.markdown("### 🎯 Key Achievements")
        st.success("✅ Identified 11.47% verified HRRP penalty cohort")
        st.success("✅ Built VCI model with 1.8x prediction accuracy")
        st.success("✅ Discovered Home Health paradox (54% rate)")
        st.success("✅ Automated ICD-9 code enrichment")
        st.success("✅ 3 actionable business recommendations")

elif page == "📊 Data Insights":
    st.markdown('<h1 class="main-header">📊 Data Analysis & Key Findings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Class Imbalance", "Risk Factors", "Operational Metrics"])
    
    with tab1:
        st.markdown("### The 'Needle in the Haystack' Challenge")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            categories = ['NO', '>30 days', '<30 days']
            values = [50000, 35000, 11000]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#2ca02c', '#ff7f0e', '#d62728']
            bars = ax.bar(categories, values, color=colors, alpha=0.8)
            
            # Remove top and right borders for a cleaner look
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            ax.set_xlabel('Readmission Category', fontsize=12)
            ax.set_ylabel('Number of Patients', fontsize=12)
            ax.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height):,}', ha='center', va='bottom', fontsize=11)
            
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.info("**Target Class:** Only 11.47% of patients are readmitted within 30 days.")
            st.warning("**The Challenge:** Simply predicting 'no readmission' gives an 89% baseline accuracy but misses every single high-risk patient.")
            st.success("**Our Goal:** Find the hidden 11% high-risk cohort driving the Medicare penalties.")
    
    with tab2:
        st.markdown("### Key Risk Factors")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💉 Medication Risk Signal")
            medications = ['No Medication', 'Oral Only', 'Insulin']
            readmission_rates = [30, 35, 49]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(medications, readmission_rates, color=['#2ca02c', '#ff7f0e', '#d62728'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_ylabel('Readmission Rate (%)', fontsize=11)
            ax.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
            st.error("**Finding:** Insulin users have a 49% readmission rate—our highest risk clinical cohort.")
        
        with col2:
            st.markdown("#### 🏥 The Home Health Paradox")
            discharge_types = ['Home', 'SNF', 'Home Health']
            rates = [46, 50, 54]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(discharge_types, rates, color=['#1f77b4', '#ff7f0e', '#d62728'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_ylabel('Readmission Rate (%)', fontsize=11)
            ax.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
            st.error("**Critical Finding:** Home Health Services show a 54% readmission rate—HIGHER than skilled nursing facilities.")
    
    with tab3:
        st.markdown("### Operational Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 Age Distribution")
            ages = np.random.normal(75, 10, 1000)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(ages, bins=30, color='#1f77b4', alpha=0.7, edgecolor='white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_xlabel('Patient Age', fontsize=11)
            ax.set_ylabel('Frequency', fontsize=11)
            ax.axvline(75, color='red', linestyle='--', label='Peak: 70-80 years')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig)
            plt.close()
            st.info("**Geriatric Challenge:** Peak volume at 70-80 years requires highly specific, age-appropriate interventions.")
        
        with col2:
            st.markdown("#### ⏱️ Length of Stay Analysis")
            groups = ['Readmitted', 'Not Readmitted']
            median_stay = [4, 4]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(groups, median_stay, color=['#d62728', '#2ca02c'], width=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_ylabel('Median Days in Hospital', fontsize=11)
            ax.set_ylim(0, 6)
            ax.grid(axis='y', alpha=0.3)
            
            for i, v in enumerate(median_stay):
                ax.text(i, v + 0.1, f'{v} days', ha='center', fontsize=11, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
            st.warning("**Finding:** Duration does not equal safety. Keeping patients longer does not reduce their readmission risk.")

elif page == "🎯 VCI Model":
    st.markdown('<h1 class="main-header">🎯 Vitality Complexity Index (VCI)</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Model Components")
        st.markdown("""
        Adapted from the industry-standard **LACE Index**, the VCI provides a quantifiable measure of patient risk.
        
        **Formula:**
        `VCI = [L]ength + [A]cuity + [C]omorbidities + [E]mergency History`
        """)
        
        components = pd.DataFrame({
            'Component': ['Length (L)', 'Acuity (A)', 'Comorbidities (C)', 'Emergency (E)'],
            'Description': [
                'Duration of hospital stay (14+ days = high risk)',
                'Emergency/Trauma admission vs Elective',
                'Number of concurrent diagnoses',
                'Past ER visits in 12 months'
            ],
            'Weight': ['0-7 points', '0-3 points', '0-5 points', '0-5 points']
        })
        st.dataframe(components, width='stretch', hide_index=True)
    
    with col2:
        st.markdown("### Risk Categories")
        st.success("**LOW RISK** (Score <7)\n\n9.6% readmission\n\nStandard discharge OK")
        st.warning("**MEDIUM RISK** (7-10)\n\n~13% readmission\n\nEnhanced monitoring")
        st.error("**HIGH RISK** (>10)\n\n17.1% readmission\n\nIntensive intervention")
    
    st.divider()
    
    st.markdown("### 📈 Model Validation Results")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        risk_levels = ['Low Risk', 'Medium Risk', 'High Risk']
        readmission_rates = [9.6, 13.4, 17.1]
        colors = ['#90ee90', '#ffa500', '#ff6b6b']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(risk_levels, readmission_rates, color=colors, alpha=0.9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel('Readmission Rate (%)', fontsize=12)
        ax.set_ylim(0, 20)
        ax.grid(axis='y', alpha=0.3)
        
        for bar, rate in zip(bars, readmission_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                   f'{rate}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 🎯 Key Result")
        st.markdown("""
        <div style='background-color: #fff9fa; padding: 2rem; border-radius: 8px; border-left: 5px solid #d32f2f; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
            <h2 style='color: #d32f2f; margin: 0; font-weight: 700;'>1.8x Higher Risk</h2>
            <p style='font-size: 1.1rem; margin-top: 1rem; color: #333'>
                High-risk patients are nearly <strong>TWICE as likely</strong> to be readmitted compared to low-risk patients.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("""
        **Business Impact:** The model successfully identifies which patients need intensive support before discharge, 
        enabling targeted interventions where they matter most and directly mitigating HRRP penalties.
        """)

elif page == "💡 Recommendations":
    st.markdown('<h1 class="main-header">💡 Strategic Recommendations</h1>', unsafe_allow_html=True)
    st.markdown("### Three evidence-based interventions to reduce readmissions")
    st.markdown("<br>", unsafe_allow_html=True)
    
    rec1, rec2, rec3 = st.columns(3)
    
    with rec1:
        st.markdown("""
        <div style='background-color: #f8fbff; padding: 1.5rem; border-radius: 8px; border: 1px solid #e1effe; border-top: 4px solid #1976d2; box-shadow: 0 4px 6px rgba(0,0,0,0.02); height: 100%;'>
            <h3 style='color: #1976d2; margin-top: 0;'>🎯 Digital Triage</h3>
            <p style='margin-top: 1rem; color: #444; font-size: 0.95rem;'>
                Integrate the VCI scoring model into the clinical dashboard with automated alerts for scores > 10, 
                enabling proactive intervention prior to discharge.
            </p>
            <hr style='border-top: 1px solid #e1effe;'>
            <p style='color: #222; font-size: 0.9rem;'><strong>Impact:</strong> Focus expensive case management resources directly on the 11.47% cohort that drives penalties.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rec2:
        st.markdown("""
        <div style='background-color: #fffbf5; padding: 1.5rem; border-radius: 8px; border: 1px solid #ffedd5; border-top: 4px solid #f57c00; box-shadow: 0 4px 6px rgba(0,0,0,0.02); height: 100%;'>
            <h3 style='color: #f57c00; margin-top: 0;'>🏥 Home Health Audit</h3>
            <p style='margin-top: 1rem; color: #444; font-size: 0.95rem;'>
                Mandate a 24-hour follow-up contact protocol for all Home Health discharges to immediately address 
                the 54% readmission failure rate.
            </p>
            <hr style='border-top: 1px solid #ffedd5;'>
            <p style='color: #222; font-size: 0.9rem;'><strong>Impact:</strong> Close the critical operational gap where patients are currently falling through the cracks.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rec3:
        st.markdown("""
        <div style='background-color: #fdfafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #f3e8ff; border-top: 4px solid #7b1fa2; box-shadow: 0 4px 6px rgba(0,0,0,0.02); height: 100%;'>
            <h3 style='color: #7b1fa2; margin-top: 0;'>💉 Insulin Mastery</h3>
            <p style='margin-top: 1rem; color: #444; font-size: 0.95rem;'>
                Implement a mandatory "Teach-Back" education track for insulin-dependent patients, 
                replacing the current, inadequate 15-minute protocols.
            </p>
            <hr style='border-top: 1px solid #f3e8ff;'>
            <p style='color: #222; font-size: 0.9rem;'><strong>Impact:</strong> Directly address the root cause of failure for our highest-risk clinical cohort (49% rate).</p>
        </div>
        """, unsafe_allow_html=True)

else:  # About page
    st.markdown('<h1 class="main-header">📁 About This Project</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Project Overview
        
        This healthcare analytics project was developed to help hospitals identify high-risk patients 
        before discharge, reducing costly readmissions and Medicare penalties.
        
        **Technical Stack:**
        - **Python** - Core programming language
        - **Pandas & NumPy** - Data manipulation and analysis
        - **Matplotlib & Seaborn** - Data visualization
        - **BeautifulSoup & Requests** - Web scraping for ICD-9 codes
        - **Streamlit** - Interactive dashboard development
        
        **Key Features:**
        1. Automated data cleaning pipeline
        2. ICD-9 code enrichment via web scraping
        3. Custom VCI risk scoring model
        4. Comprehensive data visualizations
        5. Strategic business recommendations
        
        ### Team
        - Praveen Rusiru
        - Ruwani Ranthika
        - Dinan Themika
        - Chanuth Dewhan
        
        **Academic Context:**
        - Program: GDSE 72
        - Institution: IJSE - Institute of Software Engineering
        - Lecturer: Mr. Dasun Athukorala
        """)
    
    with col2:
        st.markdown("### 📊 Project Stats")
        st.metric("Patients Analyzed", "101,766")
        st.metric("Clean Dataset", "96,437")
        st.metric("ICD-9 Codes Enriched", "20")
        st.metric("Risk Categories", "3")
        st.metric("Recommendations", "3")
        
        st.divider()
        st.markdown("### 🔗 Resources")
        st.markdown("""
        - [GitHub Repository](https://github.com/chanuthdewhan/clinical-risk-stratification)
        - [Strategic Report](https://github.com/chanuthdewhan/clinical-risk-stratification/blob/main/reports/strategic_insight_report.pdf)
        """)
        
        st.divider()
        st.info("💬 **Let's Connect!** Feel free to reach out to discuss the findings or collaborate on data engineering and full-stack projects.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; padding: 1rem;'>
    <p>Built with 🩺 for better patient outcomes | © 2026 GDSE 72 Team</p>
    <p style='font-size: 0.85rem;'>Strategic Patient Risk Stratification Project</p>
</div>
""", unsafe_allow_html=True)