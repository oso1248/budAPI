import re

# Limits to 8 characters minimun, Uppercase, Lowercase, Number, Special Character [#?!@$%^&*-]
user_password_regex = re.compile(
    r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

# Limits to list
user_role_regex = re.compile(
    r'\b(Admin|Brew Master|Assist Brew Master|BPM|PE Brewhouse|PE Finishing|Maintenance|Material Handler|Lead Brewer|Brewer|Apprentice|Weekender|Seasonal)\b')

# Limits to FTC
user_brewery_regex = re.compile(
    r'\b(FTC)\b')

# Limits to  Alphanumeric characters, 5-50 characters in length
user_name_regex = re.compile(r'^[a-zA-Z0-9\x20]{5,50}$')

# Limits to  Alphanumeric characters, 5-50 characters in length, no spaces
user_username_regex = re.compile(r'^[a-zA-Z0-9]{5,50}$')
