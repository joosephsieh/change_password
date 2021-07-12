import math, re
from collections import Counter
from difflib import SequenceMatcher


def validate_password_with_system(password):
    return True


def validate_password_scheme(password):
    if not re.match(r"^[\w\d!@#$&*]{18,}$", password):
        return False, "At least 18 alphanumeric characters and list of special chars !@#$&*."
    if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$&*]).*$", password):
        return False, "At least 1 upper case, 1 lower case ,1 numeric, and 1 special character."
    counter = Counter(password)
    if len([c for c in counter if counter[c] > 1]) > 4:
        return False, "No duplicate repeat characters more than 4."
    letters = sum(counter[c] for c in counter if c.isalpha())
    if len(password) - letters > 4:
        return False, "No more than 4 special characters."
    numbers = sum(counter[c] for c in counter if c.isdigit())
    if numbers >= math.ceil(len(password) / 2):
        return False, "50 % of password should not be a number"
    return True, "It's valid password."


def validate_password_change(old, new):
    matcher = SequenceMatcher(None,old, new)
    if matcher.ratio >= 0.8:
        return False, "Password should not similar to old password over 80% match."
    return True, "It't not similar."


def validate_password(old, new):
    if not validate_password_with_system(old):
        return False, "Old password doesn't match with system."
    result, message = validate_password_scheme(new)
    if not result:
        return result, message
    if not validate_password_change(old, new):
        return False, "Password should not similar to old password over 80% match."
    return True, "Password is valid."


def save_password(password):
    return True
