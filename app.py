import streamlit as st
import os
import pyttsx3
import speech_recognition as sr
import utils as u
from PIL import Image
from dotenv import load_dotenv
import streamlit.components.v1 as components
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Streamlit app configuration
st.set_page_config(page_title="Chatbot Demo", layout='wide')

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
input_text1 = st.text_area("Chat Input:", key='input_text_area')

# Capture voice input on button click
if st.button("Voice Command"):
    voice_input = u.speech_to_text()
    if voice_input:
        st.session_state["voice_input"] = voice_input
        st.text("You: " + voice_input)

# Button to ask the question and store responses in session state
if st.button("Send"):
    voice_input = st.session_state.get("voice_input", "")
    if input_text1:
        response = u.get_gemini_response(input_text1)
        st.session_state["response"] = response
        st.text("You: " + input_text1)
    elif voice_input:
        response = u.get_gemini_response(voice_input)
        st.session_state["response"] = response
        st.text("You: " + voice_input)
    else:
        st.warning("Please enter a question or use the microphone to ask a question.")
    
    if "response" in st.session_state:
        st.text("Chatbot: " + st.session_state["response"])

# Section for Speak Response options
st.subheader("Speak Response")
speak_text_input = st.checkbox("Speak Text Input")
speak_response = st.checkbox("Speak Response")

# Button to trigger text-to-speech based on selections
if st.button("Speak Response"):
    try:
        if speak_text_input:
            u.text_to_speech(input_text1)
        if speak_response and "response" in st.session_state:
            u.text_to_speech(st.session_state["response"])
    except Exception as e:
        st.error("An error occurred while converting text to speech. Please try again.")

# Section for Three.js cube rendering
st.subheader("3D Model Viewer")

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Three.js Red Cube</title>
  <style>
    body { margin: 0; }
    canvas { display: block; }
  </style>
</head>
<body>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script>
    // Create scene
    const scene = new THREE.Scene();

    // Set up camera
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    // Set up renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Add lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 2); // soft white light
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5).normalize();
    scene.add(directionalLight);

    // Create a red cube
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;
      renderer.render(scene, camera);
    };

    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
"""

components.html(html_code, height=600)
