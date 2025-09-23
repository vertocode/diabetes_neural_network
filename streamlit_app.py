"""
Streamlit app for Diabetes Prediction API
"""
import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
    }
    .high-risk {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        color: #d32f2f;
    }
    .low-risk {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        color: #2e7d32;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
    }
    .metric-card h4 {
        color: #000000 !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        color: #000000 !important;
        font-size: 0.95rem;
        margin: 0.3rem 0;
        line-height: 1.4;
    }
    .metric-card strong {
        color: #000000 !important;
        font-weight: 700;
    }
    .prediction-card h2 {
        color: #000000 !important;
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .prediction-card p {
        color: #000000 !important;
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    .prediction-card strong {
        color: #000000 !important;
        font-weight: 700;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .stMetric > div {
        color: #333 !important;
    }
    .stMetric label {
        color: #666 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    .stMetric div[data-testid="metric-value"] {
        color: #333 !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }
    .stMetric div[data-testid="metric-delta"] {
        color: #666 !important;
        font-size: 0.8rem !important;
    }
    .stAlert {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #000000 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #000000 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #000000 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #000000 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    /* Forçar texto preto em todos os alertas */
    .stAlert * {
        color: #000000 !important;
    }
    .stSuccess * {
        color: #000000 !important;
    }
    .stWarning * {
        color: #000000 !important;
    }
    .stError * {
        color: #000000 !important;
    }
    /* Melhorar legibilidade geral */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    .stSelectbox > div > div, .stSlider > div > div, .stNumberInput > div > div {
        color: #ffffff !important;
    }
    /* Labels e placeholders brancos para todos os inputs */
    .stSelectbox label, .stSlider label, .stNumberInput label, 
    .stTextInput label, .stTextArea label, .stDateInput label,
    .stTimeInput label, .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    /* Placeholders brancos */
    .stSelectbox input::placeholder, .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #ffffff !important;
        opacity: 0.7 !important;
    }
    /* Valores dos inputs em branco */
    .stSelectbox > div > div, .stSlider > div > div, .stNumberInput > div > div,
    .stTextInput > div > div, .stTextArea > div > div {
        color: #ffffff !important;
    }
    /* Valores dos sliders em branco */
    .stSlider > div > div > div {
        color: #ffffff !important;
    }
    /* Dropdown options em branco */
    .stSelectbox [data-baseweb="select"] {
        color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        color: #ffffff !important;
    }
    /* Forçar texto branco em todos os elementos do sidebar */
    .css-1d391kg {
        color: #ffffff !important;
    }
    .css-1d391kg label {
        color: #ffffff !important;
    }
    .css-1d391kg div {
        color: #ffffff !important;
    }
    /* Elementos específicos do Streamlit */
    .stSelectbox, .stSlider, .stNumberInput, .stTextInput, .stTextArea {
        color: #ffffff !important;
    }
    .stSelectbox *, .stSlider *, .stNumberInput *, .stTextInput *, .stTextArea * {
        color: #ffffff !important;
    }
    /* Valores dos sliders específicos */
    .stSlider [data-testid="stSlider"] {
        color: #ffffff !important;
    }
    .stSlider [data-testid="stSlider"] * {
        color: #ffffff !important;
    }
    /* Dropdown values */
    .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    /* Form labels específicos */
    .stForm label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    /* Forçar texto preto em todos os cards customizados */
    .metric-card * {
        color: #000000 !important;
    }
    .prediction-card * {
        color: #000000 !important;
    }
    /* Garantir que elementos específicos do Streamlit tenham texto preto */
    .stAlert div, .stSuccess div, .stWarning div, .stError div {
        color: #000000 !important;
    }
    .stAlert span, .stSuccess span, .stWarning span, .stError span {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def make_prediction(patient_data):
    """Make prediction using the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict",
            json=patient_data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Please make sure the API is running on localhost:8000")
        return None
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Diabetes Prediction System</h1>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("❌ API is not running. Please start the API server first:")
        st.code("cd app && python run.py", language="bash")
        st.stop()
    
    # Sidebar
    st.sidebar.title("Patient Information")
    st.sidebar.markdown("Enter the patient's health metrics below:")
    
    # Input form
    with st.sidebar.form("patient_form"):
        gender = st.selectbox("Gender", ["Female", "Male"], format_func=lambda x: f"{'👩' if x == 'Female' else '👨'} {x}")
        age = st.slider("Age", min_value=0, max_value=120, value=45)
        hypertension = st.selectbox("Hypertension", ["No", "Yes"], format_func=lambda x: f"{'❌' if x == 'No' else '⚠️'} {x}")
        heart_disease = st.selectbox("Heart Disease", ["No", "Yes"], format_func=lambda x: f"{'❌' if x == 'No' else '⚠️'} {x}")
        bmi = st.slider("BMI (Body Mass Index)", min_value=10.0, max_value=100.0, value=25.0, step=0.1)
        hba1c_level = st.slider("HbA1c Level", min_value=0.0, max_value=20.0, value=5.2, step=0.1)
        blood_glucose_level = st.slider("Blood Glucose Level", min_value=0.0, max_value=500.0, value=120.0, step=1.0)
        is_smoker = st.selectbox("Smoking Status", ["No", "Yes"], format_func=lambda x: f"{'❌' if x == 'No' else '🚬'} {x}")
        
        submitted = st.form_submit_button("🔍 Predict Diabetes Risk", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Patient Assessment")
        
        if submitted:
            # Prepare data for API
            patient_data = {
                "gender": 1 if gender == "Male" else 0,
                "age": float(age),
                "hypertension": 1 if hypertension == "Yes" else 0,
                "heart_disease": 1 if heart_disease == "Yes" else 0,
                "bmi": float(bmi),
                "hba1c_level": float(hba1c_level),
                "blood_glucose_level": float(blood_glucose_level),
                "is_smoker": 1 if is_smoker == "Yes" else 0
            }
            
            # Make prediction
            with st.spinner("Analyzing patient data..."):
                prediction_result = make_prediction(patient_data)
            
            if prediction_result:
                # Display prediction results
                prediction = prediction_result["prediction"]
                probability = prediction_result["probability"]
                confidence = prediction_result["confidence"]
                
                # Risk level
                risk_level = "HIGH RISK" if prediction == 1 else "LOW RISK"
                risk_color = "#f44336" if prediction == 1 else "#4caf50"
                risk_icon = "⚠️" if prediction == 1 else "✅"
                
                # Prediction card
                card_class = "high-risk" if prediction == 1 else "low-risk"
                st.markdown(f"""
                <div class="prediction-card {card_class}">
                    <h2>{risk_icon} {risk_level}</h2>
                    <p><strong>Probability:</strong> {probability:.1%}</p>
                    <p><strong>Confidence:</strong> {confidence}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed metrics
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                
                with col_metric1:
                    st.metric(
                        label="Diabetes Risk",
                        value=f"{probability:.1%}",
                        delta=f"{confidence} confidence"
                    )
                
                with col_metric2:
                    st.metric(
                        label="Prediction",
                        value=risk_level,
                        delta="Neural Network"
                    )
                
                with col_metric3:
                    st.metric(
                        label="Model Performance",
                        value="96.92%",
                        delta="Recall Score"
                    )
                
                # Risk factors analysis
                st.markdown("### Risk Factors Analysis")
                
                risk_factors = []
                if age > 65:
                    risk_factors.append(f"Age ({age} years) - Advanced age increases risk")
                if bmi > 30:
                    risk_factors.append(f"BMI ({bmi:.1f}) - Obesity increases risk")
                if hba1c_level > 6.5:
                    risk_factors.append(f"HbA1c ({hba1c_level}%) - Elevated levels indicate diabetes")
                if blood_glucose_level > 140:
                    risk_factors.append(f"Blood Glucose ({blood_glucose_level} mg/dL) - High levels increase risk")
                if hypertension == "Yes":
                    risk_factors.append("Hypertension - Associated with diabetes risk")
                if heart_disease == "Yes":
                    risk_factors.append("Heart Disease - Cardiovascular conditions increase risk")
                if is_smoker == "Yes":
                    risk_factors.append("Smoking - Increases diabetes risk")
                
                if risk_factors:
                    for factor in risk_factors:
                        st.warning(f"⚠️ {factor}")
                else:
                    st.success("✅ No significant risk factors identified")
    
    with col2:
        st.markdown("### Model Information")
        
        # Model stats
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 Neural Network Model</h4>
            <p><strong>Architecture:</strong> 5-layer deep network</p>
            <p><strong>Performance:</strong> 96.92% recall</p>
            <p><strong>Features:</strong> 8 health metrics</p>
            <p><strong>Type:</strong> Binary classification</p>
        </div>
        """, unsafe_allow_html=True)
        
        # API Status
        st.markdown("""
        <div class="metric-card">
            <h4>🔗 API Status</h4>
            <p><strong>Status:</strong> ✅ Connected</p>
            <p><strong>Endpoint:</strong> localhost:8000</p>
            <p><strong>Response Time:</strong> &lt; 1s</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("### Quick Statistics")
        
        # Sample data for visualization
        sample_data = {
            'Risk Level': ['Low Risk', 'High Risk'],
            'Count': [75, 25]
        }
        
        fig = px.pie(
            values=sample_data['Count'], 
            names=sample_data['Risk Level'],
            title="Typical Risk Distribution",
            color_discrete_map={'Low Risk': '#4caf50', 'High Risk': '#f44336'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🏥 Diabetes Prediction System | Developed by Group 2 - Infnet Neural Networks Course | API v1.0.0</p>
        <p>⚠️ This tool is for educational purposes only. Consult healthcare professionals for medical advice.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
