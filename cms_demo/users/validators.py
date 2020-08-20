import re
from rest_framework import serializers
from .messages import Messages


def mobile_number_validator(mobile_number):
    if not (str(mobile_number).isdigit() and len(str(mobile_number))==10):
        raise serializers.ValidationError(Messages.code.get('101'))
    return mobile_number


def pin_code_validator(pin_code):
    if not (pin_code.isdigit() and len(pin_code) == 6):
        raise serializers.ValidationError(Messages.code.get('102'))
    return pin_code


def full_name_validator(full_name):
    if not (len(full_name) > 10 and len(full_name.split(' ')) == 2):
        raise serializers.ValidationError(Messages.code.get('103'))
    return full_name


def email_validator(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return email
    raise serializers.ValidationError(Messages.code.get('104'))


def password_validator(password):
    l, u, p, d = 0, 0, 0, 0
    if (len(password) >= 8):
        for i in password:

            # counting lowercase alphabets
            if (i.islower()):
                l += 1

                # counting uppercase alphabets
            if (i.isupper()):
                u += 1

                # counting digits
            if (i.isdigit()):
                d += 1

                # counting the mentioned special characters
            if (i == '@' or i == '$' or i == '_'):
                p += 1
    if (l >= 1 and u >= 1 and p >= 1 and d >= 1 and l + p + u + d == len(password)):
        return password
    raise serializers.ValidationError(Messages.code.get('105'))


def title_validation(title):
    if len(title) <= 30:
        return title
    raise serializers.ValidationError(Messages.code.get('106'))


def body_validation(body):
    if len(body) <= 300:
        return body
    raise serializers.ValidationError(Messages.code.get('107'))


def summary_validation(summary):
    if len(summary) <= 60:
        return summary
    raise serializers.ValidationError(Messages.code.get('108'))


def doc_validation(doc):
    print(doc.name)
    if not doc.name.endswith('.pdf'):
        raise serializers.ValidationError(Messages.code.get('109'))
    return doc
