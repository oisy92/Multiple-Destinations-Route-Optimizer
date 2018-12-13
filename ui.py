import os
import shutil
from OptFun import *
from colorama import init
from termcolor import colored
import time
os.system('cls')

origins = 'Brisbane Australia'
destinations = 'Hobart City Australia'
waypoints = 'Melbourne Australia-Sydney Australia'
mode = 'Driving'
depart_time = '05:10'

mainfun(origins, destinations, waypoints, mode, depart_time)
