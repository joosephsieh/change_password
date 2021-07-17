import enum, math, re
from collections import Counter
from difflib import SequenceMatcher


class StatusCode(enum.Enum):
    SUCCESS = 0
    NOT_MATCH_RULE = 1
    NOT_MATCH_COMPLEXITY = 2
    TOO_MANY_REPEAT_CHARS = 3
    TOO_MANY_SPECIAL_CHARS = 4
    TOO_MANY_NUMBERS = 5
    NOT_MATCH_CURRENT = 6
    TOO_SIMILAR_TO_CURRENT = 7


StatusCodeToMessage = {
    StatusCode.SUCCESS: "It's valid password.",
    StatusCode.NOT_MATCH_RULE: "At least 18 alphanumeric characters and list of special chars !@#$&*.",
    StatusCode.NOT_MATCH_COMPLEXITY: "At least 1 upper case, 1 lower case ,1 numeric, and 1 special character.",
    StatusCode.TOO_MANY_REPEAT_CHARS: "No duplicate repeat characters more than 4.",
    StatusCode.TOO_MANY_SPECIAL_CHARS: "No more than 4 special characters.",
    StatusCode.TOO_MANY_NUMBERS: "50 % of password should not be a number.",
    StatusCode.NOT_MATCH_CURRENT: "Old password should match with system.",
    StatusCode.TOO_SIMILAR_TO_CURRENT: "Password should not be similar to old password over 80% match."
}


def validate_password_with_system(password):
    return True


def validate_password_scheme(password):
    if not re.match(r"^[\w\d!@#$&*]{18,}$", password):
        return False, StatusCodeToMessage[StatusCode.NOT_MATCH_RULE]
    if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$&*]).*$", password):
        return False, StatusCodeToMessage[StatusCode.NOT_MATCH_COMPLEXITY]
    counter = Counter(password)
    if len([c for c in counter if counter[c] > 1]) > 4:
        return False, StatusCodeToMessage[StatusCode.TOO_MANY_REPEAT_CHARS]
    alnum = sum(counter[c] for c in counter if c.isalnum())
    if len(password) - alnum > 4:
        return False, StatusCodeToMessage[StatusCode.TOO_MANY_SPECIAL_CHARS]
    digit = sum(counter[c] for c in counter if c.isdigit())
    if digit >= math.ceil(len(password) / 2):
        return False, StatusCodeToMessage[StatusCode.TOO_MANY_NUMBERS]
    return True, StatusCodeToMessage[StatusCode.SUCCESS]


def validate_password_similarity(old, new):
    matcher = SequenceMatcher(None, old, new)
    if matcher.ratio() >= 0.8:
        return False, StatusCodeToMessage[StatusCode.TOO_SIMILAR_TO_CURRENT]
    return True, StatusCodeToMessage[StatusCode.SUCCESS]


def validate_password(old, new):
    if not validate_password_with_system(old):
        return False, StatusCodeToMessage[StatusCode.NOT_MATCH_CURRENT]
    valid, message = validate_password_scheme(new)
    if not valid:
        return valid, message
    valid, message = validate_password_similarity(old, new)
    if not valid:
        return valid, message
    return True, StatusCodeToMessage[StatusCode.SUCCESS]


def save_password(password):
    return True
