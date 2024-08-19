# Medical AI Assistant

This Streamlit application provides a medical AI chatbot using GPT-4 Vision that can analyze medical images or provide information based on described symptoms.

## Description

The Medical AI Assistant is a web application that offers two main functionalities:

1. **Image Analysis**: Users can upload medical images for analysis. The AI will identify anomalies, potential diseases, or health issues based on the image.

2. **Symptom Analysis**: Users can describe their symptoms, and the AI will provide possible causes, recommendations, and relevant health advice.

The application also allows users to ask follow-up questions based on the initial analysis.

## Features

- Image upload and analysis using GPT-4 Vision
- Symptom description and analysis
- Follow-up question functionality
- User-friendly interface built with Streamlit

## Installation

1. Clone this repository:
```
git clone https://github.com/akhilesh1709/medical-ai-assistant.git
cd medical-ai-assistant
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Set up your OpenAI API key in Streamlit secrets (for deployment) or in a `.env` file (for local development).

## Usage

To run the application locally:
```
streamlit run app.py
```
Then, open your web browser and go to `http://localhost:8501`.

## Deployment

This application is designed to be deployed on Streamlit Cloud. Make sure to set your OpenAI API key in the Streamlit Cloud secrets before deploying.

## Important Note

This AI assistant is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/akhilesh1709/medical-ai-assistant/issues) if you want to contribute.

## Author

Your Name - [Your GitHub Profile](https://github.com/akhilesh1709)
