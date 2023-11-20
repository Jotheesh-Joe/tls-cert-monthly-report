import datetime
import logging

import azure.functions as func
import socket
import ssl
context = ssl.create_default_context()

from urllib.request import Request, urlopen, ssl, socket
import os
from urllib.error import URLError, HTTPError
import json

from . import send_email


#site without http/https in the path
def cert():
    base_url = ["silver.jotheesh.com", "gold.jotheesh.com", "specialtools.jotheesh.com"]
    port = '443'

    data_arr=[]

    for hostname in base_url:
        context = ssl.create_default_context()
        expirydate = ""
        validitystartdate = ""
        domainname = ""
        issuer = ""
        try:
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    data = ssock.getpeercert()
                    #print(data)
                    expirydate = expirydate + data["notAfter"]
                    validitystartdate = validitystartdate + data["notBefore"]

                    date_time_str = expirydate
                    date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %H:%M:%S %Y %Z')
                    expiry_date = date_time_obj.date()
                    today_date_str = datetime.date.today().strftime('%Y-%m-%d')
                    today_date_date = datetime.datetime.strptime(today_date_str, '%Y-%m-%d')
                    today_date = today_date_date.date()
                    delta = expiry_date - today_date
                    diff_days = delta.days
                    att_req = ""
                    if diff_days <= 45:
                        att_req = att_req + "yes"
                    else:
                        att_req = att_req + "no"

                    domainname_data = data["subject"]
                    for domain_item in domainname_data:
                        if domain_item[0][0] == "commonName":
                            domainname = domainname + domain_item[0][1]

                    issuer_data = data["issuer"]
                    for iss_item in issuer_data:
                        if iss_item[0][0] == "organizationName":
                            issuer = issuer + iss_item[0][1]

            reqdata = {
                "expiry_date": expirydate,
                "start_date": validitystartdate,
                "domain_name": domainname,
                "issuer": issuer,
                "expiring_soon": att_req,
                "host_name": hostname
            }

            data_arr.append(reqdata)
        
        except Exception as e:
            print(hostname, e)

    #print(data_arr)
    send_email.send_mail(data_arr)