from string import Template
from datetime import datetime, timedelta
from pprint import pprint
import random
import os

six_hours_delta = timedelta(hours=6)
ten_days_delta = timedelta(days=10)
date_format_string = '%w %Y/%m/%d %H:%M:%S'

lease_data = {
    # Start & end time of a must-show lease
    'start_date_ok': (datetime.now() - six_hours_delta).strftime(date_format_string),
    'end_date_ok' : (datetime.now() + six_hours_delta).strftime(date_format_string),

    # Start & end time of a past lease
    'start_date_old': (datetime.now() - timedelta(days=10)).strftime(date_format_string),
    'end_date_old': (datetime.now() - timedelta(days=9)).strftime(date_format_string),

    # Randomized MAC
    'random_mac': ':'.join(map(lambda x: '{:02x}'.format(x), [random.randint(0, 255) for _ in range(3)]))
}

with open(os.path.join(os.path.dirname(__file__), 'dhcpd.leases.template')) as fichero:
    content = fichero.read()
    print(Template(content).substitute(lease_data))
