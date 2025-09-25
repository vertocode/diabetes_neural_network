"""
Streamlit app for Diabetes Prediction - Direct Model Loading
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime

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

@st.cache_resource
def load_model():
    """Load the trained model from notebooks/model.h5"""
    try:
        import tensorflow as tf
        
        # Path to the model file
        model_path = os.path.join('notebooks', 'model.h5')
        
        if not os.path.exists(model_path):
            st.error(f"Model file not found at {model_path}")
            return None
        
        # Load the model
        model = tf.keras.models.load_model(model_path)
        st.success("✅ Model loaded successfully!")
        return model
        
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def prepare_input_data(gender, age, hypertension, heart_disease, bmi, hba1c_level, blood_glucose_level, smoking_history):
    """Prepare input data for prediction with proper normalization and one-hot encoding"""
    # Create features in the same order as the notebook
    # Features: ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level', 
    #           'gender_Male', 'smoking_history_current', 'smoking_history_ever', 'smoking_history_former', 
    #           'smoking_history_never', 'smoking_history_not current']
    
    # Convert gender to binary (Male = 1, Female = 0)
    gender_male = 1 if gender == "Male" else 0
    
    # Convert smoking history to one-hot encoding
    smoking_current = 1 if smoking_history == "current" else 0
    smoking_ever = 1 if smoking_history == "ever" else 0
    smoking_former = 1 if smoking_history == "former" else 0
    smoking_never = 1 if smoking_history == "never" else 0
    smoking_not_current = 1 if smoking_history == "not current" else 0
    
    # Convert to array in the correct order (12 features)
    input_data = np.array([[
        age,                    # 0: age (continuous)
        hypertension,           # 1: hypertension (0 or 1)
        heart_disease,          # 2: heart_disease (0 or 1)
        bmi,                    # 3: bmi (continuous)
        hba1c_level,           # 4: hba1c_level (continuous)
        blood_glucose_level,   # 5: blood_glucose_level (continuous)
        gender_male,           # 6: gender_Male (0 or 1)
        smoking_current,       # 7: smoking_history_current (0 or 1)
        smoking_ever,          # 8: smoking_history_ever (0 or 1)
        smoking_former,        # 9: smoking_history_former (0 or 1)
        smoking_never,         # 10: smoking_history_never (0 or 1)
        smoking_not_current    # 11: smoking_history_not current (0 or 1)
    ]])
    
    # Apply StandardScaler normalization to continuous features
    # Based on the notebooks, these features are normalized: age, bmi, hba1c_level, blood_glucose_level
    continuous_features_stats = {
        'age': {'mean': 42.0, 'std': 22.5},
        'bmi': {'mean': 27.0, 'std': 6.5},
        'hba1c_level': {'mean': 5.5, 'std': 1.2},
        'blood_glucose_level': {'mean': 140.0, 'std': 40.0}
    }
    
    # Apply normalization to continuous features
    continuous_indices = [0, 3, 4, 5]  # age, bmi, hba1c_level, blood_glucose_level
    feature_names = ['age', 'bmi', 'hba1c_level', 'blood_glucose_level']
    
    for idx, feature_name in zip(continuous_indices, feature_names):
        if feature_name in continuous_features_stats:
            stats = continuous_features_stats[feature_name]
            input_data[0, idx] = (input_data[0, idx] - stats['mean']) / stats['std']
    
    return input_data

def get_confidence_level(probability):
    """Determine confidence level based on probability"""
    if probability < 0.3 or probability > 0.7:
        return "High"
    elif probability < 0.4 or probability > 0.6:
        return "Medium"
    else:
        return "Low"

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Diabetes Prediction System</h1>', unsafe_allow_html=True)
    
    # Load model
    with st.spinner("Loading diabetes prediction model..."):
        model = load_model()
    
    if model is None:
        st.error("❌ Could not load the model. Please check if model.h5 exists in the notebooks folder.")
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
        smoking_history = st.selectbox("Smoking History", 
                                     ["never", "No Info", "current", "former", "ever", "not current"], 
                                     format_func=lambda x: f"{'🚬' if x in ['current', 'former', 'ever'] else '❌'} {x}")
        
        submitted = st.form_submit_button("🔍 Predict Diabetes Risk", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Patient Assessment")
        
        if submitted:
            # Prepare data for prediction
            patient_data = {
                "gender": gender,
                "age": float(age),
                "hypertension": 1 if hypertension == "Yes" else 0,
                "heart_disease": 1 if heart_disease == "Yes" else 0,
                "bmi": float(bmi),
                "hba1c_level": float(hba1c_level),
                "blood_glucose_level": float(blood_glucose_level),
                "smoking_history": smoking_history
            }
            
            # Prepare input data
            input_data = prepare_input_data(
                patient_data["gender"],
                patient_data["age"],
                patient_data["hypertension"],
                patient_data["heart_disease"],
                patient_data["bmi"],
                patient_data["hba1c_level"],
                patient_data["blood_glucose_level"],
                patient_data["smoking_history"]
            )
            
            # Make prediction
            with st.spinner("Analyzing patient data..."):
                try:
                    prediction_proba = model.predict(input_data, verbose=0)[0][0]
                    prediction = 1 if prediction_proba > 0.5 else 0
                    confidence = get_confidence_level(prediction_proba)
                    
                    # Risk level
                    risk_level = "HIGH RISK" if prediction == 1 else "LOW RISK"
                    risk_color = "#f44336" if prediction == 1 else "#4caf50"
                    risk_icon = "⚠️" if prediction == 1 else "✅"
                    
                    # Prediction card
                    card_class = "high-risk" if prediction == 1 else "low-risk"
                    st.markdown(f"""
                    <div class="prediction-card {card_class}">
                        <h2>{risk_icon} {risk_level}</h2>
                        <p><strong>Probability:</strong> {prediction_proba:.1%}</p>
                        <p><strong>Confidence:</strong> {confidence}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed metrics
                    col_metric1, col_metric2, col_metric3 = st.columns(3)
                    
                    with col_metric1:
                        st.metric(
                            label="Diabetes Risk",
                            value=f"{prediction_proba:.1%}",
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
                            value="89%",
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
                    if smoking_history in ["current", "former", "ever"]:
                        risk_factors.append(f"Smoking History ({smoking_history}) - Increases diabetes risk")
                    
                    if risk_factors:
                        for factor in risk_factors:
                            st.warning(f"⚠️ {factor}")
                    else:
                        st.success("✅ No significant risk factors identified")
                        
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
    
    with col2:
        st.markdown("### Model Information")
        
        # Model stats
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 Neural Network Model</h4>
            <p><strong>Architecture:</strong> 3-layer deep network</p>
            <p><strong>Performance:</strong> 89% recall</p>
            <p><strong>Features:</strong> 12 health metrics</p>
            <p><strong>Type:</strong> Binary classification</p>
            <p><strong>Model:</strong> model.h5 (loaded directly)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Model Status
        st.markdown("""
        <div class="metric-card">
            <h4>🔗 Model Status</h4>
            <p><strong>Status:</strong> ✅ Loaded</p>
            <p><strong>Source:</strong> notebooks/model.h5</p>
            <p><strong>Type:</strong> Direct Loading</p>
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
        <p>🏥 Diabetes Prediction System | Developed by Group 2 - Infnet Neural Networks Course | Direct Model Loading</p>
        <p>⚠️ This tool is for educational purposes only. Consult healthcare professionals for medical advice.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()