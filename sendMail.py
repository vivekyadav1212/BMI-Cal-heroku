import os
from email.mime.text import MIMEText
import smtplib

def sendMail(email, height, weight, bmi, bmiRange, average):
    fromEmail = f"{os.environ.get('SAANBOT_USER')}"
    fromPass = f"{os.environ.get('SAANBOT_PASS')}"
    toEmail = email

    subject = "BMI Statistics"
    message = f"""\
        <html>
            <body>
                <p>
                    Hello, and thank you for using BMI Calculator. 
                    <br> 
                    Here is the data you entered: 
                    <br>
                    <ul>
                        <li>Height: {height}cm</li>
                        <li>Weight: {weight}kg</li>
                    </ul>
                    <br>
                    Based off your data, your BMI is <strong>{round(bmi, 1)}</strong>.
                    <br>
                    The current average BMI in our database is: <strong>{round(average, 1)}</strong>.
                    <br>
                    According to the chart below, your BMI is in the <strong>{bmiRange}</strong> range.
                    <br>
                    <img src="https://images.agoramedia.com/everydayhealth/gcms/BMI-in-Adults-722x406.jpg" alt="BMI_Chart">
                </p>
            </body>
        </html>
        """
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = toEmail
    msg["From"] = fromEmail

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(fromEmail, fromPass)
    gmail.send_message(msg)
