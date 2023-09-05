from smslib import Android


# Connect to the Android device
droid = Android()

# Set the IP address and port of your Android device
device_ip = "105.214.88.229"  # Replace with your Android device's IP address
device_port = 8080  # Replace with the desired port

# Connect to the device over Wi-Fi
droid.connect_wifi(device_ip, device_port)

# Check if the connection was successful
if not droid.is_connected():
    print("Failed to connect to the Android device.")
    exit()

# Function to send a text message
def send_sms(number, message):
    droid.smsSend(number, message)

# Main loop
while True:
    # Get user input for the phone number and message
    number = input("Enter the phone number: ")
    message = input("Enter the message: ")

    # Send the SMS
    send_sms(number, message)
    print("SMS sent successfully!")

    # Ask the user if they want to send another SMS
    choice = input("Do you want to send another SMS? (y/n): ")
    if choice.lower() != "y":
        break

# Disconnect from the Android device
droid.disconnect()
