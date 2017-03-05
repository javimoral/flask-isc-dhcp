from leases import app
from flask import render_template
from flask import request
from flask_paginate import Pagination, get_page_args
from . import mongo

from isc_dhcp_leases import Lease, IscDhcpLeases

@app.route("/")
def index():
    leases = IscDhcpLeases(app.config['LEASES_FILE']).get_current()
    current_leases = [lease for mac, lease in leases.items()]

    for lease in current_leases:
        lease.vendor = find_vendor(lease.ethernet[:8])

    return render_template("show_current.html.j2", title="Current Leases", leases=current_leases)

def find_vendor(vendor_id):
    formatted_vendor_id = vendor_id.replace(":", "").upper()
    vendor = mongo.db.oui.find_one({"vendor_id": formatted_vendor_id})

    return vendor["vendor_name"]

@app.route("/history", defaults={'page':1})
@app.route("/history/", defaults={'page':1})
@app.route("/history/page/<int:page>")
@app.route("/history/page/<int:page>/")
def history(page):
    event_history = mongo.db.history.find()\
        .sort("time", -1)\
        .skip((page-1) * app.config['ENTRIES_PER_PAGE'])\
        .limit(app.config['ENTRIES_PER_PAGE'])

    total_records = mongo.db.history.count()

    pagination= get_pagination(page=page,
                            per_page=app.config['ENTRIES_PER_PAGE'],
                            total=total_records,
                            record_name='leases',
                            format_total=True,
                            format_number=True)

    return render_template("show_history.html.j2",
                title="History",
                events=event_history,
                pagination=pagination)


def get_pagination(**kwargs):
    return Pagination(css_framework='bootstrap3',
                        link_size='sm',
                        show_single_page=True,
                        **kwargs)
