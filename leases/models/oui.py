# http://stackoverflow.com/questions/8068138/process-txt-file-into-dictionary-python-v2-7
class OUI:
    def __init__(self, filename):
        with open(filename) as inputfile:
            data = inputfile.read()
            entries = data.split("\n\n")[1:-1] #ignore first and last entries, they're not real entries

            self.oui_dict = {}
            for entry in entries:
                parts = entry.split("\n")[1].split("\t")
                company_id = parts[0].split()[0]
                company_name = parts[-1]
                self.oui_dict[company_id] = company_name

    def get_vendor_string(self, macaddress):
        formatedmacaddress = macaddress.replace(':', '').upper();

        try:
            return self.oui_dict[formatedmacaddress]
        except KeyError:
            return ""
