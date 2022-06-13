import cv2
import numpy as np
import smtplib  # for sending email
import playsound
import threading
import africastalking

Alarm_Status = False
Email_Status = False
Sms_Status = False
Fire_Reported = 0
# initial

africastalking.initialize(
    username="", api_key="",
)

sms = africastalking.SMS
# response = sms.send("Hello Message!", [""])
# print(response)


def play_alarm_sound_function():
    while True:
        playsound.playsound("alarm-sound.mp3", True)


# sms
def sending():
    # Set the numbers in international format
    recipients = [""]
    # Set your message
    message = (
        "There is a FIRE in Diamond Heights Floor Number 2! Evacuate the building now! "
    )
    # Set your shortCode or senderId
    # sender = "XXYYZZ"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f"Houston, we have a problem: {e}")


def send_mail_function():

    recipientEmail = ""
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("Your Email", "Password")
        server.sendmail(
            "recepient mail",
            recipientEmail,
            "Warning A Fire Accident has been reported on your premises.",
        )
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
        print(e)


video = cv2.VideoCapture(0)  # bonfire.mp4  capture video

while True:
    (grabbed, frame) = video.read()  # extract frames from the video
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))  # resizing the output window

    # applying blur to remove noises
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    # converting the flame into hsv formats
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # defining the colour of the fire
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")  # convert into numpy value
    upper = np.array(upper, dtype="uint8")  # convert into numpy value

    mask = cv2.inRange(hsv, lower, upper)  # looking for the two colors

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)  # measuring the size of the fire

    if (
        int(no_red) > 10000
    ):  # if the size of the fire exceeds 1500 then fire is reported
        Fire_Reported = Fire_Reported + 1

    cv2.imshow("fire_detector", output)  # the output window

    # turn on the alarm sound
    if Fire_Reported >= 1:

        if Alarm_Status == False:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True

        if Email_Status == False:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True
        if Sms_Status == False:
            threading.Thread(target=sending).start()
            Sms_Status = True

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
video.release()
