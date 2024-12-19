import speech_recognition as sr
import pyttsx3
import requests
import cv2
import face_recognition
import time

# Speech Recognition Function
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

# Text-to-Speech Function
def speak_response(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

# Function to Search on the Internet
def search_on_internet(query):
    api_key = "YOUR_GOOGLE_API_KEY"
    cx = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    
    response = requests.get(url)
    search_results = response.json()
    if "items" in search_results:
        first_result = search_results["items"][0]
        return first_result["title"], first_result["link"]
    return "No results found.", ""

# Facial Recognition Function
def recognize_face():
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture image.")
            break
        
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if face_locations:
            print("Face recognized!")
            video_capture.release()
            cv2.destroyAllWindows()
            return "John Doe"  # Example: replace with actual recognition logic
        else:
            print("No face detected.")
            cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return None

# Main Function to Combine Everything
def main():
    # Listen for command
    user_command = listen_for_command()
    
    if user_command:
        # Recognize the face
        person_name = recognize_face()
        
        # Greet the person if recognized
        if person_name:
            greet_message = f"Hello, {person_name}! How can I assist you today?"
        else:
            greet_message = "Hello! How can I assist you today?"
        
        speak_response(greet_message)

        # Perform search or other tasks based on user command
        if "search" in user_command.lower():
            query = user_command.replace("search", "").strip()
            title, link = search_on_internet(query)
            speak_response(f"Here is what I found: {title}. You can read more at {link}.")
        else:
            speak_response("Sorry, I did not understand that command.")
    else:
        speak_response("I could not hear any command.")
    
if __name__ == "__main__":
    main()
