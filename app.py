import random
import os
from flask import Flask, render_template_string, request, make_response, render_template
import pdfkit

pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
output_path = '/Users/samrat/VsCode/POS_Project/output.pdf'

app = Flask(__name__)


@app.route('/pdf', methods=['POST'])
def generate_pdf():
    billnos = random.randrange(577890, 900000, 6)
    billdate = request.form['billdate']
    rate = 98.21
    volume = 35.00
    total = (rate*volume)

    # Generate the HTML code with the user inputs
    with open('index.html', 'r') as f:
        html_template = f.read()
    html = render_template_string(html_template, billno=billnos, billdate=billdate, rate=rate, volume=volume, total=total)

    # Generate the PDF from the HTML code
    pdf = pdfkit.from_string(html, output_path)

    # Return the PDF file as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response

if __name__ == '__main__':
    app.run()
