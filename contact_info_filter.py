# contact_info_filter.py
# by Matt Ciocchi
# Last updated 8/14/2012.
#
# contact_info_filter.py is a short script written to filter garbage entries out of a database that has been exported to .csv format.

import csv, re, sys

# First, the program needs to access the legacy database with Python. (You may need to change these paths to point at the correct files.)

legacy_access_database = open("/home/mciocchi/Projects/data_transformation/sandbox/legacy_access_database.csv", 'r')
legacydatareader = csv.DictReader(legacy_access_database,)

# Next, a new empty file needs to be created. This is where the filtered data will be written to disk.

legacy_access_database_filtered = open("/home/mciocchi/Projects/data_transformation/sandbox/legacy_access_database_filtered.csv", 'w')
filtereddatawriter = csv.DictWriter(legacy_access_database_filtered, ['ContactID', 'ContactName', 'AddressLine1', 'AddressLine2', 'City', 'StateProv', 'ZIPPostalCode', 'Phone', 'EMail', ], )

# Discarded data will be written to a third file, to be sorted through by hand later, in case some of it is salvageable:

legacy_access_database_discarded_data = open("/home/mciocchi/Projects/data_transformation/sandbox/legacy_access_database_discarded_data.csv", 'w')
discardeddatawriter = csv.DictWriter(legacy_access_database_discarded_data, ['ContactID', 'ContactName', 'AddressLine1', 'AddressLine2', 'City', 'StateProv', 'ZIPPostalCode', 'Phone', 'EMail', ], )


def isgarbage(csvline):
    """
    Take one line of a csv file and put it through a series of tests to determine whether it is garbage data. Returns True if the contact information is useless, and False otherwise.
    """

# Pull data from the dictionary csvline into variables inside this closure for the purpose of readability and simplicity.

    ContactName = csvline.get('ContactName')
    AddressLine1 = csvline.get('AddressLine1')
    AddressLine2 = csvline.get('AddressLine2')
    City = csvline.get('City')
    Phone = csvline.get('Phone')
    EMail = csvline.get('EMail')

    def discarddata():
        """
        Discarded lines are written to a separate file for further processing.
        """
        discardeddatawriter.writerow(csvline)

    def isemptystring(string):
        """
        Check to see if a string is 'empty,' e.g., if it is whitespace or an empty pair of quotes. Return True if the string is empty, and False otherwise.
        """
        if bool(string.strip(" ,\t,\r")) is False:
            return True
        else:
            return False

    def isbadaddress(string):
        """
        Search string for variations and misspellings of the phrase "bad address," return True if there is a match and False otherwise.
        """
        if re.search('bad.*ad+res+|ad+res+.*bad', string, flags=re.IGNORECASE, ) is None:
            return False
        else:
            return True

    def addresslinesunusable():
        """
        Checks if AddressLine1 and AddressLine2 are usable. Returns True if they are, False otherwise.
        """
        def eitheraddresslinebad():
            if isbadaddress(AddressLine1) or isbadaddress(AddressLine2):
                return True
            else:
                return False

        def bothaddresslinesempty():
            if isemptystring(AddressLine1) and isemptystring(AddressLine2):
                return True
            else:
                return False

        if isemptystring(City):
            return True
        elif eitheraddresslinebad() or bothaddresslinesempty():
            return True
        else:
            return False

    def iswithoutcontactinfo():
        """
        Check to see if there is any way to contact the individual. Returns a boolean.
        """
        if addresslinesunusable() and isemptystring(Phone) and isemptystring(EMail):
            return True
        else:
            return False

    if iswithoutcontactinfo():
        discarddata()
    elif isemptystring(ContactName):
        discarddata()
    else:
        filtereddatawriter.writerow(csvline)

for line in legacydatareader:
    isgarbage(line)

legacy_access_database.close()
legacy_access_database_filtered.close()
legacy_access_database_discarded_data.close()
sys.exit(0)
