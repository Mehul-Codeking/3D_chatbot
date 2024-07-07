import streamlit as st
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import utils as u

# Load environment variables
load_dotenv()

# Initialize Streamlit app configuration
st.set_page_config(page_title="Chatbot Demo", layout='wide')


# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background: url('https://wallpapercave.com/wp/wp2747953.jpg') no-repeat center center fixed;
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

# Initialize interests in session state if not already done
if "interests" not in st.session_state:
    st.session_state["interests"] = []

# Initialize the chatbot's initial greeting
if "initial_greeting" not in st.session_state:
    st.session_state["initial_greeting"] = True
    st.session_state["conversation"] = ["Chatbot: My name is Shastra. How are you doing today?"]
    st.text("Chatbot: My name is Shastra. How are you doing today?")

# Section for user input
st.subheader("User Input")
input_text1 = st.text_area("Chat Input:", key='input_text_area')

# Capture voice input on button click
if st.button("Voice Command"):
    voice_input = u.speech_to_text()
    if voice_input:
        st.session_state["voice_input"] = voice_input
        st.session_state["conversation"].append("You: " + voice_input)
        st.text("You: " + voice_input)

# Input for user interests
st.subheader("User Interests")
input_interests = st.text_input("Enter your interests (comma-separated):", key='input_interests')

# Update interests on button click
if st.button("Update Interests"):
    interests = input_interests.split(',')
    st.session_state["interests"] = update_interests(st.session_state["interests"], interests)
    st.text(f"Current interests: {', '.join(st.session_state['interests'])}")

# Button to ask the question and store responses in session state
if st.button("Send"):
    voice_input = st.session_state.get("voice_input", "")
    if input_text1:
        response = u.get_gemini_response(input_text1, st.session_state["interests"])
        st.session_state["conversation"].append("You: " + input_text1)
        st.session_state["conversation"].append("Chatbot: " + response)
        st.session_state["interests"] = u.update_interests(st.session_state["interests"], input_text1)
        st.text("You: " + input_text1)
    elif voice_input:
        response = u.get_gemini_response(voice_input, st.session_state["interests"])
        st.session_state["conversation"].append("You: " + voice_input)
        st.session_state["conversation"].append("Chatbot: " + response)
        st.session_state["interests"] = u.update_interests(st.session_state["interests"], voice_input)
        st.text("You: " + voice_input)
    else:
        st.warning("Please enter a question or use the microphone to ask a question.")
    
    if "conversation" in st.session_state:
        for message in st.session_state["conversation"]:
            st.text(message)

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

# Section for Three.js polygraphic person rendering
st.subheader("3D Model Viewer")

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Three.js Polygraphic Person</title>
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

    // Function to create a wireframe sphere
    function createWireframeSphere(radius, widthSegments, heightSegments, color) {
      const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
      const material = new THREE.MeshBasicMaterial({ color: color, wireframe: true });
      return new THREE.Mesh(geometry, material);
    }

    // Function to create a wireframe cylinder
    function createWireframeCylinder(radiusTop, radiusBottom, height, radialSegments, color) {
      const geometry = new THREE.CylinderGeometry(radiusTop, radiusBottom, height, radialSegments);
      const material = new THREE.MeshBasicMaterial({ color: color, wireframe: true });
      return new THREE.Mesh(geometry, material);
    }

    // Create polygraphic person
    const head = createWireframeSphere(0.5, 16, 16, 0xff0000);
    head.position.y = 1.6;
    scene.add(head);

    const body = createWireframeCylinder(0.3, 0.3, 1, 16, 0x00ff00);
    body.position.y = 0.8;
    scene.add(body);

    const leftArm = createWireframeCylinder(0.1, 0.1, 0.8, 16, 0x0000ff);
    leftArm.position.set(-0.75, 1.2, 0);
    leftArm.rotation.z = 1.5;
    scene.add(leftArm);

    const rightArm = createWireframeCylinder(0.1, 0.1, 0.8, 16, 0x0000ff);
    rightArm.position.set(0.75, 1.2, 0);
    rightArm.rotation.z = -1.5;
    scene.add(rightArm);

    const leftLeg = createWireframeCylinder(0.1, 0.1, 1, 16, 0xffff00);
    leftLeg.position.set(-0.25, -0.5, 0);
    scene.add(leftLeg);

    const rightLeg = createWireframeCylinder(0.1, 0.1, 1, 16, 0xffff00);
    rightLeg.position.set(0.25, -0.5, 0);
    scene.add(rightLeg);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      head.rotation.y += 0.01;
      body.rotation.y += 0.01;
      leftArm.rotation.y += 0.01;
      rightArm.rotation.y += 0.01;
      leftLeg.rotation.y += 0.01;
      rightLeg.rotation.y += 0.01;
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
