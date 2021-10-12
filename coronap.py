from bs4 import BeautifulSoup
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from time import sleep

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path



getPage = requests.get('https://virus-korona.sk/api.php')
soup = getPage.text
test = json.loads(soup)
num_infected=(test['tiles']['k26']['data']['d'][len(test['tiles']['k26']['data']['d'])-1]['v'])
print(num_infected)

 
# img = Image.new('RGB', (100, 30), color = (73, 109, 137))
img = Image.open('coronafin.png') 
font = ImageFont.truetype(r'/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',85)
d = ImageDraw.Draw(img)
d.text((365,562), str(num_infected), fill=(206,111,49), font=font)
 
img.save('pil_text.png')




email = 'jankooomakak@gmail.com' # Your email
password = 'mAkak321k' # Your email account password
send_to_email = ['janko@gmail.com', 'test2@gmail.com','test@gmail.com'] # Who you are sending the message to
rec =  ', '.join(send_to_email)
subject = 'Počet prípadov COVID-19'
message = 'Počet prípadov na Slovensku je dnes: '+ str(num_infected) # The message in the email
file_location = 'pil_text.png'

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = rec
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

# Setup the attachment
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# Attach the attachment to the MIMEMultipart object
msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
