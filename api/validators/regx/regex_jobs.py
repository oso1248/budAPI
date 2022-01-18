import re

# Limits to  Alphanumeric characters, 5-25 characters in length
jobs_name_regex = re.compile(
    r'^[a-zA-Z0-9\x20]{5,25}$')

# Limits to Brewhouse, Finishing only
jobs_area_regex = re.compile(
    r'\b(Brewhouse|Finishing)\b')
