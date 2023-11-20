# TimerTrigger - Python

This function monitors list of urls given to it and send a monthly update of whether the ssl certificates for the given urls are expiring in near future

## How it works

The python azure function app will run on the first day of every month and check the expiry date of all URLs given to it and send a mail with the help of sendgrid to the platform team.

