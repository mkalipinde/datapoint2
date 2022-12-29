import random
import datetime
from datetime import timedelta
from .models import *


class UrlHelper:
    def view_url(self, process_code):
        if (process_code == "IE"):
            return 'it-equipment'

        elif (process_code == "SR"):
            return 'sap-right'

        elif (process_code == "NE"):
            return 'new-employee'

        elif (process_code == "SR"):
            return 'sap-right'

        elif (process_code == "WC"):
            return 'workflow-change'  



        elif (process_code == "AM"):
            return 'asset-movement'

        elif (process_code == "AFP"):
            return 'afp'

        elif (process_code == "ES"):
            return 'expense-sheet'

        elif (process_code == "MJR"):
            return 'manual-journal-request' 

        elif (process_code == "PW"):
            return 'payable-waiver'

        elif (process_code == "AD"):
            return 'asset-disposal'

        elif (process_code == "GOC"):
            return 'goc'



        elif (process_code == "OT"):
            return 'overtime'

        elif (process_code == "MD"):
            return 'mileage' 

        elif (process_code == "TA"):
            return 'travel'



        elif (process_code == "VC"):
            return 'vendor'

        elif (process_code == "ST"):
            return 'stationery'

        else:
            return False    
