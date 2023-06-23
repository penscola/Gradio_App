import gradio as gr
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

# Load the saved full pipeline from the file
full_pipeline = joblib.load('pipe.pkl')

# Define the predict function
def predict(gender, SeniorCitizen, Partner, Dependents, Contract, tenure, MonthlyCharges,
            TotalCharges, PaymentMethod, PhoneService, MultipleLines, InternetService,
            OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV,
            StreamingMovies, PaperlessBilling):
    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'gender': [gender] if gender else ['Male'],  # Replace None with default value
        'SeniorCitizen': [SeniorCitizen] if SeniorCitizen is not None else [0],  # Replace None with default value
        'Partner': [Partner] if Partner else ['No'],  # Replace None with default value
        'Dependents': [Dependents] if Dependents else ['No'],  # Replace None with default value
        'tenure': [tenure] if tenure else [1],  # Replace None with default value
        'PhoneService': [PhoneService] if PhoneService else ['Yes'],  # Replace None with default value
        'MultipleLines': [MultipleLines] if MultipleLines else ['No'],  # Replace None with default value
        'InternetService': [InternetService] if InternetService else ['DSL'],  # Replace None with default value
        'OnlineSecurity': [OnlineSecurity] if OnlineSecurity else ['No'],  # Replace None with default value
        'OnlineBackup': [OnlineBackup] if OnlineBackup else ['No'],  # Replace None with default value
        'DeviceProtection': [DeviceProtection] if DeviceProtection else ['No'],  # Replace None with default value
        'TechSupport': [TechSupport] if TechSupport else ['No'],  # Replace None with default value
        'StreamingTV': [StreamingTV] if StreamingTV else ['No'],  # Replace None with default value
        'StreamingMovies': [StreamingMovies] if StreamingMovies else ['No'],  # Replace None with default value
        'Contract': [Contract] if Contract else ['Month-to-month'],  # Replace None with default value
        'PaperlessBilling': [PaperlessBilling] if PaperlessBilling else ['No'],  # Replace None with default value
        'PaymentMethod': [PaymentMethod] if PaymentMethod else ['Electronic check'],  # Replace None with default value
        'MonthlyCharges': [MonthlyCharges] if MonthlyCharges else [0.0],  # Replace None with default value
        'TotalCharges': [TotalCharges] if TotalCharges else [0.0]  # Replace None with default value
    })


        # Make predictions using the loaded logistic regression model
    predictions = full_pipeline.predict(input_data)

    #return predictions[0]
    if predictions[0] == "Yes":
        return "Churn"
    else:
        return "Not Churn"

# Setting Gradio App Interface
with gr.Blocks(css=".gradio-container {background-color: grey}") as demo:
    gr.Markdown("# Teleco Customer Churn Prediction #\n*This App allows the user to predict whether a customer will churn or not by entering values in the given fields. Any field left blank takes the default value.*")
    
    # Receiving ALL Input Data here
    gr.Markdown("**Demographic Data**")
    with gr.Row():
        gender = gr.Dropdown(label="Gender", choices=["Male", "Female"])
        SeniorCitizen = gr.Radio(label="Senior Citizen", choices=[1, 0])
        Partner = gr.Radio(label="Partner", choices=["Yes", "No"])
        Dependents = gr.Radio(label="Dependents", choices=["Yes", "No"])

    gr.Markdown("**Service Length and Charges (USD)**")
    with gr.Row():
        Contract = gr.Dropdown(label="Contract", choices=["Month-to-month", "One year", "Two year"])
        tenure = gr.Slider(label="Tenure (months)", minimum=1, step=1, interactive=True)
        MonthlyCharges = gr.Slider(label="Monthly Charges", step=0.05)
        TotalCharges = gr.Slider(label="Total Charges", step=0.05)

    # Phone Service Usage part
    gr.Markdown("**Phone Service Usage**")
    with gr.Row():
        PhoneService = gr.Radio(label="Phone Service", choices=["Yes", "No"])
        MultipleLines = gr.Dropdown(label="Multiple Lines", choices=[
                                    "Yes", "No", "No phone service"])

    # Internet Service Usage part
    gr.Markdown("**Internet Service Usage**")
    with gr.Row():
        InternetService = gr.Dropdown(label="Internet Service", choices=["DSL", "Fiber optic", "No"])
        OnlineSecurity = gr.Dropdown(label="Online Security", choices=["Yes", "No", "No internet service"])
        OnlineBackup = gr.Dropdown(label="Online Backup", choices=["Yes", "No", "No internet service"])
        DeviceProtection = gr.Dropdown(label="Device Protection", choices=["Yes", "No", "No internet service"])
        TechSupport = gr.Dropdown(label="Tech Support", choices=["Yes", "No", "No internet service"])
        StreamingTV = gr.Dropdown(label="TV Streaming", choices=["Yes", "No", "No internet service"])
        StreamingMovies = gr.Dropdown(label="Movie Streaming", choices=["Yes", "No", "No internet service"])

    # Billing and Payment part
    gr.Markdown("**Billing and Payment**")
    with gr.Row():
        PaperlessBilling = gr.Radio(
            label="Paperless Billing", choices=["Yes", "No"])
        PaymentMethod = gr.Dropdown(label="Payment Method", choices=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

    # Output Prediction
    output = gr.Text(label="Outcome")
    submit_button = gr.Button("Predict")
    
    submit_button.click(fn= predict,
                        outputs= output,
                        inputs=[gender, SeniorCitizen, Partner, Dependents, Contract, tenure, MonthlyCharges, TotalCharges, PaymentMethod, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, PaperlessBilling],
    
    ),
    
    # Add the reset and flag buttons
    
    def clear():
        output.value = ""
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
         
    clear_btn = gr.Button("Reset", variant="primary")
    clear_btn.click(fn=clear, inputs=None, outputs=output)
        
 
demo.launch(inbrowser = True)