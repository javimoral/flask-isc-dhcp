#!/usr/bin/env python
import sys
from pymongo import MongoClient

if __name__ == "__main__":
    """ Los argumentos vienen en el siguiente orden
        0: Nombre del script (omitimos)
        1: Tipo de evento
        2: IP asignada
        3: Dirección MAC
        4: Hostname
    """

    arguments = ["eventType", "assignedIP", "macAddress", "hostname"]

    collection = MongoClient().leases.history
    collection.insert_one(dict(zip(arguments, sys.argv[1:])))
