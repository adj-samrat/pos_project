import random
from typing import Final
from flask import make_response

# pip install python-telegram-bot
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jinja2 import Template
import pdfkit

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

print('Starting up bot...')

billDate =''
billTime =''
rate = ''
volume = ''

TOKEN: Final = '6075679203:AAHUmpteC7mKr47AFTWY-hO0c3bJpViLAYc'
BOT_USERNAME: Final = '@Fuelbill_bot'
config= pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
output_path = '/Users/samrat/VsCode/POS_Project/output.pdf'

# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello Sandy! I\'m a fuel bill generator bot. Do you want to Generate a bill? Type -Yes')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.chat_id)
    await context.bot.send_document(chat_id=update.message.chat_id, document=open('output.pdf', 'rb'))
    await update.message.reply_text('Thankyou for not disturbing Samrat!! Bye for Now!')
   


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def handle_response(text: str) -> str:
    # Create your own response logic
    billnos = random.randrange(577890, 900000, 6)
   
    processed: str = text.lower()
    print (processed)

    if 'hello' in processed:
        return 'Hey there! Use Start Command to Generate Bill'

    if 'yes' in processed:
        return 'To Generate Bill , Type - Billdate = DD/MMM/YYYY, e.g Billdate = 13/01/2023'

    if 'billdate ' in processed:
        
       global billDate
       billDate = processed.split("=")[1].strip()
       return 'Type Billtime = HH:MM:SS, e/.g/. Billtime = 10:13:49'
    
    if 'billtime ' in processed:
        
        global billTime
        billTime = processed.split("=")[1].strip()
        return 'Type Rate = XX.XX, e/.g/. Rate = 99.10'
    
    if 'rate ' in processed:
        
      global rate 
      rate = processed.split("=")[1].strip()
      return 'Type Volume = XX.XX, e/.g/. Volume = 35.00'

    
    if 'volume' in processed:
     # Generate the HTML code with the user inputs
     global volume
     global pdf
     volume = processed.split("=")[1].strip()
     total = float(rate) * float(volume)
     with open('index.html', 'r') as f:
            html_template = Template(f.read())
     html = html_template.render ( billno=billnos, billTime=billTime, billdate=billDate, rate=rate, volume=volume, total=total)

        # Generate the PDF from the HTML code
     try:   
      pdf = pdfkit.from_string(html, output_path, configuration = config)
     except Exception as error:
        #response = make_response('output.pdf')
       # response.headers['Content-Type'] = 'application/pdf'
       # response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

        # Send the PDF response back to the user
     #Bot.send_document(chat_id=Update.message.chat.id, document=response.content)
        print('Testing',error)
        handle_message()
     #sendMail()
    
    return 'Thanks for using Samrat bot. Now Click on Send PDF Command to get the PDF!' 
   
    return 'I don\'t understand'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('send_pdf', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)

def sendMail ():

# Set the email parameters
    sender_email = 'samrattheraja@gmail.com'
    sender_password = 'rockerrocker'
    recipient_email = 'srm.samrat@gmail.com'
    subject = 'Fuel Bill'
    body = 'Please find attached the PDF document.'

# Define the PDF file path and name
    pdf_file_path = '/Users/samrat/VsCode/POS_Project/output.pdf'
    pdf_file_name = os.path.basename(pdf_file_path)

# Open the PDF file in binary mode and read its content
    with open(pdf_file_path, 'rb') as f:
        pdf_content = f.read()

# Create a MIME multipart message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

# Attach the body of the email
    msg.attach(MIMEText(body))

# Attach the PDF file to the email
    pdf_part = MIMEApplication(pdf_content, Name=pdf_file_name)
    pdf_part['Content-Disposition'] = f'attachment; filename="{pdf_file_name}"'
    msg.attach(pdf_part)

# Connect to the SMTP server and login with the sender's credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)

    # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

# Print a message to confirm the email was sent
    print(f'Email with PDF attachment sent to {recipient_email}')