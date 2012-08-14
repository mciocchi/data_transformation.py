# data_transformation.py
# by Matt Ciocchi
# Last updated 8/14/2012.
#
# data_transformation.py is a Python script that converts a legacy database exported to csv format into a new schema.

import csv, sys

# First, the program needs to access the legacy database with Python, and store that interface as a variable.
legacy_access_database_filtered = open("/home/mciocchi/Projects/data_transformation/sandbox/legacy_access_database_filtered.csv", 'r')
legacydatareader = csv.DictReader(legacy_access_database_filtered,)

# Next, a new empty file needs to be created. This is where the filtered data will be written to disk.
transformed_data = open("/home/mciocchi/Projects/data_transformation/sandbox/transformed_data.csv", 'w')

transformeddatawriter = csv.DictWriter(transformed_data,  ['Id', 'FirstName', 'LastName', 'Street', 'City', 'State', 'ZipCode', 'Country', 'Phone', 'Email', 'LegacyName', 'LegacyAddressFirstLine', 'LegacyAddressSecondLine', 'LegacyID', ], quoting=csv.QUOTE_ALL)


def transform(legacyline):
    """
    Assign legacy data to the fields of the new database. Takes in a line of the legacy database in the form of a dictionary from csv.DictReader. Returns a csv dictionary transformed into the new schema.
    """
    transformedline = {'Id': '', 'FirstName': '', 'LastName': '', 'Street': '', 'City': '', 'State': '', 'ZipCode': '', 'Country': '', 'Phone': '', 'Email': '', 'LegacyAddressFirstLine': '',  'LegacyAddressSecondLine': '',  'LegacyID': '', }
    transformedline['LegacyID'] = legacyline['ID']
    transformedline['LegacyName'] = legacyline['Name']
    transformedline['LegacyAddressFirstLine'] = legacyline['AddressFirstLine']
    transformedline['LegacyAddressSecondLine'] = legacyline['AddressSecondLine']
    transformedline['City'] = legacyline['City']
    transformedline['State'] = legacyline['State']
    transformedline['ZipCode'] = legacyline['ZIP']
    transformedline['Phone'] = legacyline['Phone']
    transformedline['Email'] = legacyline['EMail']

    SplitName = legacyline['Name'].split()
    if len(SplitName) == 2:
        """
        If the Name field is two words, it gets mapped into the FirstName and LastName fields in the new schema.
        """
        transformedline['LastName'] = SplitName.pop()
        transformedline['FirstName'] = SplitName.pop()
        transformedline['LegacyName'] = ''
        return transformedline

    else:
        """
        If the person goes by a one part name, or a compound name with more than two parts, it is programmatically very difficult to decide what to do with it, and so the name is folded into the LegacyName field.
        """
        transformedline['LegacyName'] = legacyline['Name']
        return transformedline

transformeddatawriter.writeheader()

for legacyline in legacydatareader:
    transformeddatawriter.writerow(transform(legacyline))

legacy_access_database_filtered.close()
transformed_data.close()

sys.exit(0)
