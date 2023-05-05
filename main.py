import random
from jinja2 import Template

# Define the variable
billnos = random.randrange(577890, 900000, 6)
billdate = "21/05/2023"
rate = 98.21
volume = 35.00
total = (rate*volume)

# Read the HTML file
with open("index.html", "r") as f:
    template = Template(f.read())

# Replace the placeholder with the variable

html = template.render(billno=billnos, billdate=billdate, rate=rate, volume=volume, total=total)



# Write the modified HTML to a new file
with open("output.html", "w") as f:
    f.write(html)
