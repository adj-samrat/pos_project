import random
import telegram
from telegram.ext import Updater, MessageHandler
from telegram.ext import filters
from flask import Flask, render_template_string, request, make_response
import pdfkit

pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
output_path = '/Users/samrat/VsCode/POS_Project/output.pdf'


app = Flask(__name__)


@app.route('/pdf', methods=['POST'])
def generate_pdf():

    # Set up the Telegram bot
    bot_token = 'BOT_TOKEN'
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    

    # Define the function that will be called when a message is received
    def handle_message(update, context):
        # Get the message text from the user
        message_text = update.message.text
        billnos = random.randrange(577890, 900000, 6)
        # Split the message into multiple inputs
        inputs = message_text.split(',')
        billdate = inputs[0].strip()
        rate = inputs[1].strip()
        volume = inputs[2].strip()
        billTime = inputs[3].strip()
        total = (rate*volume)

        # Generate the HTML code with the user inputs
        with open('index.html', 'r') as f:
            html_template = f.read()
        html = render_template_string(html_template, billno=billnos, billTime=billTime, billdate=billdate, rate=rate, volume=volume, total=total)

        # Generate the PDF from the HTML code
        pdf = pdfkit.from_string(html, output_path)

        # Return the PDF file as a response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

        # Send the PDF response back to the user
        bot.send_document(chat_id=update.message.chat_id, document=response.content)

    # Set up the message handler
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    dispatcher.add_handler(message_handler)

    # Start the bot
    updater.start_polling()

    # Return a dummy response
    return 'PDF generation initiated'


if __name__ == '__main__':
    app.run()
