import streamlit as st
import os
import pyttsx3
import speech_recognition as sr
#from py_avataaars import PyAvataaar, AvatarStyle, SkinColor, HairColor, FacialHairType, TopType, EyesType, EyebrowType, MouthType, ClothesColor, ClothesType
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to create an avatar image
#def create_avatar(mouth_type):
    #avatar = PyAvataaar(
       #style=AvatarStyle.CIRCLE,
       #skin_color=SkinColor.LIGHT,
       #hair_color=HairColor.BLACK,
       # facial_hair_type=FacialHairType.DEFAULT,
        #top_type=TopType.SHORT_HAIR_DREADS_02,
        #eye_type=EyesType.DEFAULT,
        #eyebrow_type=EyebrowType.DEFAULT,
        #mouth_type=mouth_type,
        #clothes_color=ClothesColor.HEATHER,
        #clothes_type=ClothesType.HOODIE
    #)
    # Render avatar directly to PNG file
    #avatar.render_png_file('output_avatar.png')
    #avatar_image = Image.open('output_avatar.png')
    #return avatar_image

# Function to load GEMINI Pro Model and get response
def get_gemini_response(question):
    # Placeholder function for actual API call
    return "This is a simulated response for the question: " + question

# Function to convert text to speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
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
st.set_page_config(page_title="Chatbot Demo", layout='wide')

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background: url('https://wallpapercave.com/wp/wp2568619.jpg') no-repeat center center fixed;
        background-size: cover;
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
input_text1 = st.text_area("Chat Input:", key='input_text_area')

# Capture voice input on button click
if st.button("Voice Command"):
    voice_input = speech_to_text()
    if voice_input:
        st.session_state["voice_input"] = voice_input
        st.text("You: " + voice_input)

# Button to ask the question and store responses in session state
if st.button("Send"):
    voice_input = st.session_state.get("voice_input", "")
    if input_text1:
        response = get_gemini_response(input_text1)
        st.session_state["response"] = response
        st.text("You: " + input_text1)
    elif voice_input:
        response = get_gemini_response(voice_input)
        st.session_state["response"] = response
        st.text("You: " + voice_input)
    else:
        st.warning("Please enter a question or use the microphone to ask a question.")
    
    if "response" in st.session_state:
        st.text("Chatbot: " + st.session_state["response"])

# Display the avatar
#if "response" in st.session_state:
  #  avatar_image = create_avatar(MouthType.SMILE)  # Using a fixed mouth type for simplicity
    #st.image(avatar_image, caption='Chatbot Avatar', use_column_width=True)

# Section for Speak Response options
st.subheader("Speak Response")
speak_text_input = st.checkbox("Speak Text Input")
speak_response = st.checkbox("Speak Response")

# Button to trigger text-to-speech based on selections
if st.button("Speak Response"):
    try:
        if speak_text_input:
            text_to_speech(input_text1)
        if speak_response and "response" in st.session_state:
            text_to_speech(st.session_state["response"])
    except Exception as e:
        st.error("An error occurred while converting text to speech. Please try again.")
