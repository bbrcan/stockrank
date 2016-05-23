import datetime


def sort_list_into_keys(objects, copy_attr, sort_attr):
    """Sorts a given list of objects. Then creates a new list, which contains
    only a given attribute of each object.

    Arguments:
    copy_attr -- The attribute of each object to copy into the new list.
    sort_attr -- The attribute of each object to sort the list by.
    """
    sorted_list = sorted(objects, key=lambda x: getattr(x, sort_attr),
                         reverse=True)
    sorted_keys = [getattr(x, copy_attr) for x in sorted_list]
    return sorted_keys


def timestamp():
    """Returns the current unix timestamp.
    """
    return datetime.datetime.now().timestamp()
