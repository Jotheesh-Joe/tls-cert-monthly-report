import datetime
import logging

import azure.functions as func

from urllib.request import Request, urlopen, ssl, socket
import os
from urllib.error import URLError, HTTPError
import json

from . import certmanager

#Send mail method



def main(mytimer: func.TimerRequest) -> None:
    certmanager.cert()
