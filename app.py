import streamlit as st
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
import tempfile

load_dotenv()

# Initialize OpenAI client using Streamlit secrets
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY in Streamlit secrets.")
    st.stop()
else:
    client = OpenAI(api_key=api_key)

sample_prompt = """You are a medical practitioner and an expert in analyzing medical-related images working for a very reputed hospital. You will be provided with images and you need to identify the anomalies, any disease or health issues. You need to generate the result in a detailed manner. Write all the findings, next steps, recommendations, etc. You only need to respond if the image is related to a human body and health issues. You must answer but also write a disclaimer saying that "Consult with a Doctor before making any decisions".

Remember, if certain aspects are not clear from the image, it's okay to state 'Unable to determine based on the provided image.'

Now analyze the image and answer the above questions in the same structured manner defined above."""

symptom_prompt = """You are a medical AI assistant. A user has described their symptoms. Analyze these symptoms and provide possible causes, recommendations for next steps, and any relevant health advice. Remember to include a disclaimer stating 'This is not a substitute for professional medical advice. Please consult with a healthcare provider for an accurate diagnosis and treatment plan.'"""

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'result' not in st.session_state:
    st.session_state.result = None

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_gpt4_model_for_analysis(filename: str, sample_prompt=sample_prompt):
    base64_image = encode_image(filename)
    
    messages = [
        {
            "role": "user",
            "content":[
                {
                    "type": "text", "text": sample_prompt
                    },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                        }
                    }
                ]
            }
        ]

    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = messages,
        max_tokens = 1500
        )

    return response.choices[0].message.content

def analyze_symptoms(symptoms):
    messages = [
        {
            "role": "user",
            "content": f"{symptom_prompt}\n\nUser symptoms: {symptoms}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )

    return response.choices[0].message.content

def answer_query(query, context):
    messages = [
        {
            "role": "system",
            "content": "You are a medical AI assistant. Answer the user's query based on the previous analysis and your medical knowledge. Always include a disclaimer about consulting a real doctor."
        },
        {
            "role": "user",
            "content": f"Previous analysis: {context}\n\nUser query: {query}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )

    return response.choices[0].message.content

st.title("Medical AI Assistant")

st.write("""
This is a medical AI chatbot using GPT Vision that can analyze medical images or provide information based on symptoms you describe. 
Please note that this AI assistant is not a substitute for professional medical advice, diagnosis, or treatment. 
""")

analysis_type = st.radio("Choose analysis type:", ("Image Analysis", "Symptom Analysis"))

if analysis_type == "Image Analysis":
    uploaded_file = st.file_uploader("Upload a Medical Image", type=["jpg", "jpeg", "png"])

    # Temporary file handling
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state['filename'] = tmp_file.name

        st.image(uploaded_file, caption='Uploaded Image')

    # Process button
    if st.button('Analyze Image'):
        if 'filename' in st.session_state and os.path.exists(st.session_state['filename']):
            st.session_state['result'] = call_gpt4_model_for_analysis(st.session_state['filename'])
            st.markdown(st.session_state['result'], unsafe_allow_html=True)
            os.unlink(st.session_state['filename'])  # Delete the temp file after processing

else:
    symptoms = st.text_area("Describe your symptoms:")
    if st.button('Analyze Symptoms'):
        if symptoms:
            st.session_state['result'] = analyze_symptoms(symptoms)
            st.markdown(st.session_state['result'], unsafe_allow_html=True)

# Additional query section
if st.session_state['result']:
    st.markdown("## Do you have any other questions?")
    additional_query = st.text_input("Enter your question here:")
    if st.button('Get Answer'):
        if additional_query:
            answer = answer_query(additional_query, st.session_state['result'])
            st.markdown("### Answer:")
            st.markdown(answer, unsafe_allow_html=True)