import datetime 
import os
import sys

def dateme():
    parser = datetime.datetime.now()
    return parser.strftime("%m-%d-%Y")