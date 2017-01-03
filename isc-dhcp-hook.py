#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hook for ISC DHCP
Should be called with execute when an event is generated
"""

import sys
import datetime

from pymongo import MongoClient

if __name__ == "__main__":
    """ Los argumentos vienen en el siguiente orden
        0: Nombre del script (omitimos)
        1: Tipo de evento
        2: IP asignada
        3: Dirección MAC
        4: Hostname
    """

    arguments = ["eventType", "assignedIP", "macAddress", "hostname", "leaseDuration"]

    collection = MongoClient().leases.history
    record = dict(zip(arguments, sys.argv[1:]))
    record["time"] = datetime.datetime.now()
    collection.insert_one(record)
