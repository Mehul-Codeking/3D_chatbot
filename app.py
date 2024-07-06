import streamlit as st
import os
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables (assuming you have a `.env` file)
load_dotenv()

# Configure Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load GEMINI Pro Model and get response
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.text.replace("*", "")  # Remove asterisks before returning

# Function to convert text to speech (without asterisks)
def text_to_speech(text):
    engine = pyttsx3.init()  # Initialize pyttsx3 engine
    engine.say(text.replace("*", ""))  # Remove asterisks before speaking
    engine.runAndWait()

# Function to transcribe speech to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
    try:
        user_input = r.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Initialize Streamlit app configuration
st.set_page_config(page_title="Chatbot Demo")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background: url('https://wallpapercave.com/wp/wp2568619.jpg') no-repeat center center fixed;
        background-size: cover;
        padding-top: 50px; /* Ensure content starts below the header */
    }
    body {
        background: none;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    .stTextInput, .stTextArea {
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
    }
    .stHeader, .stSubheader {
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("ChatBot Demo")

# Section for user input
st.subheader("User Input")

# Display the input text
input_text1 = st.text_area("Chat Input:")

# Capture voice input on button click
if st.button("Voice Command"):
    voice_input = speech_to_text()
    if voice_input:
        st.session_state["voice_input"] = voice_input
        st.text("You: ")
        st.text(voice_input)

# Button to ask the question and store responses in session state
if st.button("Send"):
    # Ensure voice_input is fetched from session state
    voice_input = st.session_state.get("voice_input", "")
    if input_text1:  # Check if user input text is not empty
        response = get_gemini_response(input_text1)
        st.session_state["response"] = response  # Update session state for response
        st.text("You:")
        st.text(input_text1)
    elif voice_input:  # Check if voice input is not empty
        response = get_gemini_response(voice_input)
        st.session_state["response"] = response  # Update session state for response
        st.text("You:")
        st.text(voice_input)
    else:
        st.warning("Please enter a question or use the microphone to ask a question.")
    
    # Display chatbot response after checking for either input
    if "response" in st.session_state:
        st.text("Chatbot:")
        st.text(st.session_state["response"])

# Section for Speak Response options
st.subheader("Speak Response")
speak_text_input = st.checkbox("Speak Text Input")
speak_response = st.checkbox("Speak Response")

# Button to trigger text-to-speech based on selections
if st.button("Speak Response"):
    try:
        if speak_text_input:
            text_to_speech(input_text1)  # Speak text input if checkbox is selected
        if speak_response and "response" in st.session_state:
            text_to_speech(st.session_state["response"])  # Speak response if checkbox is selected and exists
    except Exception as e:
        st.error("An error occurred while converting text to speech. Please try again.")
