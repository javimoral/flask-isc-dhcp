from .leases import mongo

def find_vendor(lease):
    vendor_id = lease.ethernet[:8]
    formatted_vendor_id = vendor_id.replace(":", "").upper()
    vendor = mongo.db.oui.find_one({"vendor_id": formatted_vendor_id})
    lease.vendor = vendor["vendor_name"]

    return lease

__all__ = ['find_vendor']