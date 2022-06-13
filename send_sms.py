import africastalking

# TODO: Initialize Africa's Talking


africastalking.initialize(
    username="felixmilgo21",
    api_key="e72d407ea008ed1b491444fbbcfa888f042c23ebc5e7e3ee46ecf61a9274e8bd",
)

sms = africastalking.SMS
# response = sms.send("Hello Message!", ["+254727541692"])
# print(response)


class send_sms:
    def sending(self):
        # print("sending...")
        # Set the numbers in international format
        recipients = ["+254727541692"]
        # Set your message
        message = "Kunawaka manzee!!!!"
        # Set your shortCode or senderId
        sender = "XXYYZZ"
        try:
            response = sms.send(message, recipients)
            print(response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")


send_sms().sending()
# recipients = ["+254727541692"]
# message = "Kunawaka manzee!!!!"


# def on_finish(error, response):
#     if error is not None:
#         raise error
#     print(response)


# sms.send(message, recipients, callback=on_finish)
