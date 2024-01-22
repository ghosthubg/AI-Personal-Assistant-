#aido is an (Artificial Intelligence Digital Organizer)

#Import modules
import pyttsx3
import speech_recognition as sr
import time
from plyer import notification
from bs4 import BeautifulSoup
import requests
import openai
from email.message import EmailMessage
import smtplib
#initialisation
engine = pyttsx3.init()
engine.setProperty('volume', 0.8)

#AI INTRO

#user's name stored in a variable called 'user_name'
user_name = "Andrew"
engine.say(f"Hello {user_name}! I am Aido, your personal  assistant.")
engine.say("designed to help you organise and automate your life.")
engine.say("Let's get started, what would you like to do?")
engine.runAndWait()


#create an instance for speech recognition
recognizer = sr.Recognizer()
#set up listener and capture audio from microphone
with sr.Microphone() as source:
    print("Listening")
    audio = recognizer.listen(source)

#perform speech recognition from captured audio

try:
    recognized_text = recognizer.recognize_google(audio)
    print("You said:", recognized_text)
    if "appointment" in recognized_text:
        # Ask for appointment details
        engine.say("Sure! Please provide the details of the appointment.")
        engine.runAndWait()
        #set instance

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        # Listen for the appointment details
        appointment_details = recognizer.recognize_google(audio)

        # Add appointment to the list
        with open("list.txt", "a") as file:
            file.write(f"{appointment_details}\n")

        # Confirmation message
        engine.say("Appointment set!")
        engine.runAndWait()
        print("Appointment set:", appointment_details)

        engine.say("\nYour current appointment is " + appointment_details)
        engine.runAndWait()

        #delete item in appointment
    elif "delete" in recognized_text:
        # Ask for appointment details
        engine.say("Sure! Please provide the item you want to delete.")
        engine.runAndWait()
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        # Listen for the appointment details
        item_to_remove = recognizer.recognize_google(audio)
        # get_item_user_wants_to_delete
        with open("list.txt", "r") as file:  # read  item from list
            lines = file.readlines()
        updated_lines = []  # if line is not in line update with current lines
        item_deleted = False  # set to false as nothing has been deleted
        for line in lines:  # iterate over each line
            if item_to_remove not in line:
                updated_lines.append(line)  # if line does not exist append current
            else:
                item_deleted = True
        # if item was found and deleted rewrite file with updated lines
        if item_deleted:
            with open("list.txt", "w") as file:
                file.writelines(updated_lines)
                print("Item deleted: ", item_to_remove)
                engine.say("item deleted was " + item_to_remove)
                engine.runAndWait()
                # Announce the updated list
                engine.say("Your Updated list Contains:")
                for line in updated_lines:
                    engine.say(line.rstrip())
                engine.runAndWait()


        else:
            engine.say("item not found in list")
            engine.runAndWait()
            print("Item not found in the list.")
            #updating items in appointments
    elif "replace" in recognized_text:
        engine.say("Sure! Please provide the item you want to replace.")
        engine.runAndWait()
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        # Listen for the appointment details
        item_to_replace = recognizer.recognize_google(audio)
        with open("list.txt", "r+") as file:
            contents = file.read()
            engine.say(f"Sure! what do want to replace {item_to_replace} with.")
            engine.runAndWait()
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)
            # Listen
            new_item = recognizer.recognize_google(audio)
            updated_contents = contents.replace(item_to_replace, new_item)
            engine.say("list has been updated with" + new_item)
            engine.runAndWait()
            print("list has been updated  with: ", new_item)
            file.seek(0)
            file.write(updated_contents)
            file.truncate()
        file.close()
    #get list of items in appointment

    elif "list" in recognized_text:

        engine.say("Sure! here is your list.")
        engine.runAndWait()
        with open("list.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                engine.say(line.rstrip())
                engine.runAndWait()
                print("Updated list: ", line.rstrip())
# set reminder
    elif "reminder" in recognized_text:
        engine.say("Sure! which item and when.")
        engine.runAndWait()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        # Listen
        reminder = recognizer.recognize_google(audio)

        with open("list.txt", "r") as file:
            lines = file.readlines()
            updated_lines = []  # if line is not in line update with current lines
            item_found = False  # set to false as nothing has been deleted
            for line in lines:  # iterate over each line
                if reminder not in line:
                    updated_lines.append(line)  # if line does not exist append current
                else:
                    item_found = True
    # if item was found and deleted rewrite file with updated lines
            if item_found:
                engine.say("in how many minutes?")
                engine.runAndWait()
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source)
                # Listen
                user_time = recognizer.recognize_google(audio)
                local_time = float(user_time)
                local_time = local_time * 60
                time.sleep(local_time)
                engine.say("its time for your appointment" + reminder)
                engine.runAndWait()
                print(reminder)
                #notifications
    elif "notification" in recognized_text:
    # Ask for item to notify
        engine.say("Sure! Please provide the item you want to be notified.")
        engine.runAndWait()

    # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

    # Listen for the item to notify
            item_to_notify = recognizer.recognize_google(audio)

            item_found = False

            with open("list.txt", "r") as file:
                for line in file:
                    if item_to_notify in line:
                        item_found = True
                        break

            if item_found:

                notification.notify(
                    title='Notification',
                    message=item_to_notify,
                    app_icon=None,
                    timeout=10,
                )
                print("Notification created for:", item_to_notify)
                engine.say("Notification created for: " + item_to_notify)
                engine.runAndWait()
            else:
                print("Item not found in the list.")
                engine.say("Item not found in the list")
                engine.runAndWait()


except sr.UnknownValueError:
    engine.say("sorry l did not understand what you said")
    engine.runAndWait()
    print("could not understand the audio.")

except sr.RequestError as e:
    print(f"could not request results from google;{e}")

 #WEATHER
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', 0.8)

    def get_user_response(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            recognized_text = self.recognizer.recognize_google(audio)
            print("You said:", recognized_text)
            return recognized_text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return ""

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def fetch_weather(self, city):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        city = city.replace(" ", "+")
        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        print("Searching...\n")
        soup = BeautifulSoup(res.text, 'html.parser')

        location = soup.select('#wob_loc')
        time = soup.select('#wob_dts')
        info = soup.select('#wob_dc')
        weather = soup.select('#wob_tm')

        if location and time and info and weather:
            print(location[0].getText().strip())
            print(time[0].getText().strip())
            print(info[0].getText().strip())
            print(weather[0].getText().strip() + "°C")
            self.speak("Weather information for " + location[0].getText().strip() + " is " + weather[0].getText().strip() + " degrees Celsius.")
        else:
            print("Weather information not found.")
            self.speak("Sorry, I could not retrieve the weather information.")

    def start(self):
        self.speak("Please provide your city to fetch the weather.")
        city = self.get_user_response()

        if city:
            city = city + " weather"
            self.fetch_weather(city)
            self.speak("Have a nice day!")

class AIAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', 0.8)
        self.openai_api_key = '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'

    def get_user_response(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            recognized_text = self.recognizer.recognize_google(audio)
            print("You said:", recognized_text)
            return recognized_text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return ""

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def ai_interaction(self):
        messages = [{"role": "system", "content": "You are an intelligent assistant."}]
        while True:
            self.speak("Ask me a question.")
            message = self.get_user_response()
            if message:
                messages.append({"role": "user", "content": message})
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    api_key=self.openai_api_key
                )
                reply = chat.choices[0].message.content
                self.speak(reply)
                print(f"ChatGPT: {reply}")
                messages.append({"role": "assistant", "content": reply})

    def start(self):
        self.speak("How can I assist you?")
        self.ai_interaction()

# Instantiate the voice assistant and AI assistant
voice_assistant = VoiceAssistant()
ai_assistant = AIAssistant()

# Start the voice assistant


#email automation

def get_user_response():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        # Use Google Web Speech API for speech recognition
        recognized_text = recognizer.recognize_google(audio)
        print("You said:", recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return ""


def speak(text):
    engine.say(text)
    engine.runAndWait()


def send_email(sender, password, recipient, subject, body):
    try:
        # Set up the SMTP connection
        smtp_server = "smtp.gmail.com"
        port = 587
        smtp_connection = smtplib.SMTP(smtp_server, port)
        smtp_connection.starttls()
        smtp_connection.login(sender, password)

        # Compose the email
        email_message = EmailMessage()
        email_message["From"] = sender
        email_message["To"] = recipient
        email_message["Subject"] = subject
        email_message.set_content(body)

        # Send the email
        smtp_connection.send_message(email_message)
        print("Email sent successfully!")
        speak("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        speak("Sorry, an error occurred while sending the email.")

    finally:
        # Close the SMTP connection
        smtp_connection.quit()


# Example usage
sender_email = "syloncube837@gmail.com"
sender_password = ""

speak("Please provide the recipient's email address.")
recipient_email = get_user_response()

if recipient_email:
    speak("Please provide the email subject.")
    email_subject = get_user_response()

    speak("Please provide the email body.")
    email_body = get_user_response()

    send_email(sender_email, sender_password, recipient_email, email_subject, email_body)
    speak("Have a nice day!")

#integrate IOT Devices

