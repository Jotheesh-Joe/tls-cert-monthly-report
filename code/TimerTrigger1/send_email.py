import json
import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime


def send_mail(data):
    mydate = datetime.datetime.now()
    month = (mydate.strftime("%B"))
    year = mydate.strftime("%Y")
    email_body_html = """<html>    
        <style>
        #ExpiredCerts {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        #ExpiredCerts td, #ExpiredCerts th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        #ExpiredCerts tr:nth-child(even){background-color: #ddd;}
        #ExpiredCerts th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #245494;
            color: white;
        }
        footer {
            text-align: center;
            padding: 3px;
            background-color: Blue;
            color: white;
        }
        </style>"""

    email_body_html += f"""<body>
            <p>Dear Platform Team,</p>
            <p>Certificate expiry report for the month of {month} {year} follows:</p>
        <table id="ExpiredCerts">
        <tr>
          <th>Domain Name</th>
          <th>Validity - Start Date</th>
          <th>Validity - Expiry Date</th>
          <th>Expiring Soon - 45 days or less</th>
          <th>Issuer</th>
          <th>URL Used To Validate</th>
        </tr>
            """

    for item in data:
        if item['expiring_soon'] == 'yes':
            id_color = '#DA4355'
        else:
            id_color = '#8BDA66'
        email_body_html += f"""        <tr>
                                            <td>{item['domain_name']}</td>
                                            <td>{item['start_date']}</td>
                                            <td>{item['expiry_date']}</td>
                                            <td style="background-color:{id_color}">{item['expiring_soon']}</td>
                                            <td>{item['issuer']}</td>
                                            <td>{item['host_name']}</td>
                                           </tr>"""

    email_body_html += """  </table>
            <br/>
            <p>Please take action and renew the certificates if required.</p>
            <br/>
            <div id=""fonttag"">
            <b> Best Regards,
            <br/> Platform Cloud Team | <a href=mailto:joe7mailbox@gmail.com?Subject=Need-Assistance>Platform Team</a>
            </b></p></div><br/>
            <footer>
            <p>**This is an automated mail please dont reply to this email**</p>
            </footer>
            </body>
            </html>
                """

    message = Mail(
        from_email='no-reply@jotheeswaran.local',
        to_emails=['joe7mailbox@gmail', 'joemailbox77@gmail.com'],
        subject='Platform TLS Certificate - Monthly Report',
        html_content=email_body_html)

    sendgrid_api_key = os.environ["sendgrid_api_key"]
    sg = SendGridAPIClient(sendgrid_api_key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)