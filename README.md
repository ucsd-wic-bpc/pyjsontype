pyjsontypes
===========
A Python library for extracting type information from JSON-represented data.
This library was originally built to be used by
[PyCFramework](https://github.com/ucsd-wic-bpc/pycframework) in its template-
generation system.


Supported Types
---------------
All supported types are defined in `jsontypes.py`. A short list is given as:

  * Integers
  * Floats
  * Strings
  * Chars
  * Booleans
  * Lists (of any of the aforementioned types)


Usage
-----
pyjsontypes has two methods which can be used to deduce types from JSON data.
The parsing methods are defined in `parse.py`.

### parse.get_type(str) ###
Takes in JSON-formatted data and returns the type of the data. If the type of
data cannot be deduced, `None` is returned.

```py
parse.get_type("hello world")  # returns JSONTypes.STRING

parse.get_type("1")  # returns JSONTypes.INT

parse.get_type("1.0")  # returns JSONTypes.FLOAT

parse.get_type('[["true"]]')  # returns JSONContainer(JSONContainer(JSONTypes.BOOL))
```

### parse.resolve_type(list) ###
Takes in a list of JSON-formatted data where each element should be of the same
type. Returns the type of all elements. If elements' types conflict or if the
types cannot be deduced, `None` is returned.

```py
parse.resolve_type(["a"])  # returns JSONTypes.CHAR

parse.resolve_type(["a", "hello"])  # returns JSONTypes.STRING

parse.resolve_type(["1", "2", "3"])  # returns JSONTypes.INT

parse.resolve_type(["1", "2", "3.14159"])  # returns JSONTypes.FLOAT

parse.resolve_type(["1", "hello"])  # returns None
```
