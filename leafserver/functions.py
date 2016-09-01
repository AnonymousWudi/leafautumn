# coding=utf-8

from django.http import Http404
from django.shortcuts import get_object_or_404


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    try:
        ret = get_object_or_404(klass, *args, **kwargs)
    except Http404:
        return None
    else:
        return ret


def get_int(value):
    try:
        result = int(value)
    except ValueError:
        result = 0
    return result
