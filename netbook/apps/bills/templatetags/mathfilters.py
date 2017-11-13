# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django import template
from django.template.base import resolve_variable, Node, TemplateSyntaxError
from decimal import Decimal

register = template.Library()

#
# Custom filters
#
def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg
    try:
        return int(arg)
    except ValueError:
        return float(arg)


@register.filter(name='sub')
def sub(value, arg):
    """Subtracts the arg from the value."""
    try:
        return valid_numeric(value) - valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''
sub.is_safe = False


@register.filter(name='mul')
def mul(value, arg):
    """Multiplies the arg with the value."""
    try:
        return valid_numeric(value) * valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ''
mul.is_safe = False


@register.filter(name='div')
def div(value, arg):
    """Divides the arg by the value."""
    try:
        return valid_numeric(value) / valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value / arg
        except Exception:
            return ''
div.is_safe = False


@register.filter(name='abs')
def absolute(value):
    """Returns the absolute value."""
    try:
        return abs(valid_numeric(value))
    except (ValueError, TypeError):
        try:
            return abs(value)
        except Exception:
            return ''
absolute.is_safe = False

@register.filter(name='sqrt')
def sqrt(value):
    """Returns the absolute value."""
    try:
        return sqrt(valid_numeric(value))
    except (ValueError, TypeError):
        try:
            return sqrt(value)
        except Exception:
            return ''
absolute.is_safe = False



#
# Custom Tags
#
class MulTag(Node):
    def __init__(self,numList):
        self.numList = numList

    def render(self, context):
        realList = []
        try:
            for numobj in self.numList:
                realList.append(numobj.resolve(context))
        except:
            raise TemplateSyntaxError("multag error")
        try:
            value = realList[0]
            for num in realList[1:]:
                value = value* num
            return round(value,2)
        except:
            return ''

@register.tag(name="mmul")
def getMulNums(parser, token):
    bits = token.contents.split()
    realList = [parser.compile_filter(x) for x in bits[1:]]
    return MulTag(realList)
