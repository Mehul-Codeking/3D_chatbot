import pyttsx3
import speech_recognition as sr
import google.generativeai as genai


def text_to_speech(text):
    engine = pyttsx3.init()  # Initialize pyttsx3 engine
    engine.say(text.replace("*", ""))  # Remove asterisks before speaking
    engine.runAndWait()

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

def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.text.replace("*", "")  # Remove asterisks before returning