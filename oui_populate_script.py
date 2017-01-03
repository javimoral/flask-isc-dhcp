#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Populate OUI database with the content of the oui.txt file
http://stackoverflow.com/questions/8068138/process-txt-file-into-dictionary-python-v2-7
"""

from pymongo import MongoClient

collection = MongoClient().leases.oui

with open("oui.txt") as inputfile:
    data = inputfile.read()
    entries = data.split("\n\n")[1:-1] #ignore first and last entries, they're not real entries
    oui_dict = {}
    for entry in entries:
        parts = entry.split("\n")[1].split("\t")
        company_id = parts[0].split()[0]
        company_name = parts[-1]
        oui_item = {"vendor_id": company_id, "vendor_name": company_name}
        collection.insert_one(oui_item)
        oui_dict[company_id] = company_name
