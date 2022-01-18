import re

# Limits to  Alphanumeric characters, 5-50 characters in length
commodity_name_regex = re.compile(r'^[a-zA-Z0-9\x20]{5,50}$')

# Limits to Grains|Brewhouse|Fermenting|Chips|Finishing
commodity_location_regex = re.compile(
    r'\b(Grains|Brewhouse|Fermenting|Unitanks|Chips|Finishing)\b')

# Limits to Brw|Fin|Log
commodity_inventory_regex = re.compile(
    r'\b(Brw|Fin|Log)\b')

# Limits to Numeric 8 Digits Only
commodity_sap_regex = re.compile(
    r'^[0-9]{8,8}$')
