from django import template
from os import path

register = template.Library()


def basename(value):
    value = str(value)
    return path.basename(value)


register.filter("basename", basename)
