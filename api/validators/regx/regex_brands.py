import re

# Limits to  Alphanumeric characters, 4 characters in length
brands_name_regex = re.compile(r'^[A-Z0-9]{4,4}$')


# Limits to  Alphanumeric characters, [,.], 5-50 characters in length
brands_method_regex = re.compile(r'^[a-zA-Z0-9,.\x20]{4,25}$')
