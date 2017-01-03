from leases import app
from flask import render_template
from flask import request
from . import mongo

from isc_dhcp_leases import Lease, IscDhcpLeases

import pytz
from datetime import datetime

@app.route("/")
def index():
    leases = IscDhcpLeases(app.config['LEASES_FILE']).get_current()
    current_leases = [lease for mac, lease in leases.items()]

    for lease in current_leases:
        lease.start = utc_to_local(lease.start)
        lease.end = utc_to_local(lease.end)
        lease.diff = lease.end - lease.start
        lease.start = datetime.strftime(lease.start, '%H:%M:%S')
        lease.end = datetime.strftime(lease.end, '%H:%M:%S')
        lease.vendor = \
            mongo.db.oui.find_one({"vendor_id":
                lease.ethernet[:8].replace(":", "").upper()})\
                ["vendor_name"]
    return render_template("show_current.html", title="Current Leases", leases=current_leases)

def utc_to_local(utc_dt):
   local_tz = pytz.timezone(app.config['TIMEZONE'])
   local_dt = utc_dt.replace(tzinfo = pytz.utc).astimezone(local_tz)
   return local_tz.normalize(local_dt)
