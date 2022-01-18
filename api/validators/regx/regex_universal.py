import re

# Limits to  Alphanumeric characters, [,.], 5-50 characters in length
universal_note_regex = re.compile(r'^[a-zA-Z0-9,.\x20]{0,256}$')

universal_phone_regex = re.compile(r'^[0-9]{10,10}$')
