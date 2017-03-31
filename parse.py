from jsontypes import JSONTypes, JSONContainer
import json


def nonlist_to_json_type(nonlist_type):
    """
    Converts the given type (assuming its not a JSON list) into a JSONType
    instance
    """
    if isinstance(nonlist_type, unicode):
        nonlist_type = str(nonlist_type)

    if isinstance(nonlist_type, str) and len(nonlist_type) == 1:
        return JSONTypes.CHAR
    else:
        return JSONTypes.parse(type(nonlist_type).__name__)


def list_to_json_type(jsonlist):
    """
    Converts the given list to a JSONContainer type. Note that the given list
    is assumed to be a list (or list-of-lists) where all elements in the list
    are of the same type.

    If the list's type could not be deduced, None is returned
    """
    list_depth = 0

    # Keep iterating through the list until we find a leaf element
    while isinstance(jsonlist, list):
        # We cannot determine the type from empty lists. Return None
        if len(jsonlist) == 0:
            return None

        list_depth += 1
        jsonlist = jsonlist[0]

    # Leaf element found, determine its type
    element_type = nonlist_to_json_type(jsonlist)

    # Now create the container
    while list_depth > 0:
        element_type = JSONContainer(element_type)
        list_depth -= 1

    return element_type


def get_type(jsonstr):
    """
    Return the type of the provided string. If the type cannot be determined,
    None is returned.
    """
    try:
        parsed_jsonstr = json.loads(jsonstr)
    except ValueError:
        parsed_jsonstr = jsonstr

    if isinstance(parsed_jsonstr, list):
        return list_to_json_type(parsed_jsonstr)
    else:
        return nonlist_to_json_type(parsed_jsonstr)


def get_root_type(jsontype):
    """
    Returns the root type of a JSONType. If it is a pure JSONType, the type
    iself is the root. If it is a Container, its leaf type is the root type
    """
    if isinstance(jsontype, JSONContainer):
        return jsontype.root_type
    else:
        return jsontype


def resolve_type(jsonstr_list):
    """
    Provided a list where each element should be of the same JSONType, return
    the JSONType of the elements.

    If an error occurs while resolving the type, None is returned.
    """
    strtypes = [get_type(jsonstr) for jsonstr in jsonstr_list]

    if len(strtypes) == 0:
        return None

    finalized_type = strtypes[0]
    for next_type in strtypes[1:]:

        if next_type is None:
            continue

        if finalized_type is None:
            finalized_type = next_type
            continue

        if isinstance(finalized_type, JSONContainer) and not isinstance(next_type, JSONContainer):
            return None

        if not isinstance(finalized_type, JSONContainer) and isinstance(next_type, JSONContainer):
            return None

        # If they are both lists and not the same degree, skip it
        if isinstance(finalized_type, JSONContainer) and isinstance(next_type, JSONContainer):
            if finalized_type.degree != next_type.degree:
                return None

        coerced_type = coerce_types(finalized_type, next_type)
        if coerced_type is None:
            return None

        finalized_type = coerced_type

    return finalized_type


def coerce_types(first, second):
    """
    Coerces items of two types following the coercion map. If they are the same
    type, that type is returned.

    Returns None if the types are different and cannot be coerced
    """
    first_root = get_root_type(first)
    second_root = get_root_type(second)

    if first_root == second_root:
        return first

    def should_coerce_to_first(first_root, second_root):
        if first_root == JSONTypes.STRING and second_root == JSONTypes.CHAR:
            return True

        if first_root == JSONTypes.FLOAT and second_root == JSONTypes.INT:
            return True

        return False

    if should_coerce_to_first(first_root, second_root):
        return first

    if should_coerce_to_first(second_root, first_root):
        return second

    return None
