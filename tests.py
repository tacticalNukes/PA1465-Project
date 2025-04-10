import datetime
import hashlib
import math
import pickle
from collections import namedtuple, defaultdict, OrderedDict

import numpy as np

# A tuple used for the testing
Person = namedtuple('Person', ['name', 'age', 'email'])

# Just a class for the testing
class CustomClass:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, CustomClass):
            return False
        return self.name == other.name and self.value == other.value
def get_pickle_hash(obj, protocol=None):
    data = pickle.dumps(obj, protocol)
    return hashlib.sha256(data).hexdigest()


def test_simple_types(protocol=None):
    tests = {
        "int": 42,
        "float": 3.14159265358979323846,
        "bool": True,
        "str": "Hello, World!",
        "bytes": b"Binary data",
        "none": None,
        "complex": complex(3, 4)
    }

    results = {}
    for name, value in tests.items():
        results[name] = get_pickle_hash(value, protocol)

    return results

def test_floating_point_precision(protocol=None):
    tests = {
        "floating_addition": 0.1 + 0.2,
        "pi": math.pi,
        "euler": math.e,
        "low number": 1e-10,
        "higher number": 1e10,
        "float_inf": float('inf'),
        "float_-inf": float('-inf'),
        "float_nan": float('nan')
    }
    results = {}
    for name, value in tests.items():
        try:
            results[name] = get_pickle_hash(value, protocol)
        except (pickle.PickleError, TypeError) as e:
            results[name] = f"ERROR: {type(e).__name__}: {str(e)}"

    return results

def test_numpy_special_values(protocol=None):
    tests = {
        "np_inf": np.inf,
        "np_neg_inf": -np.inf,
        "np_nan": np.nan,
        "np_float": np.float64(0.0),
        "np_float_-": np.float64(-0.0)
    }
    results = {}
    for name, value in tests.items():
        try:
            results[name] = get_pickle_hash(value, protocol)
        except (pickle.PickleError, TypeError) as e:
            results[name] = f"ERROR: {type(e).__name__}: {str(e)}"
    return results

def test_circular_references(protocol=None):
    a = []
    b = [a]
    a.append(b)

    tests = {
        "circular_ref": a,
        "nested_circular_ref": {"a": a, "b": b},
        "custom_circular_ref": CustomClass("circular", a)
    }
    results = {}
    for name, value in tests.items():
        try:
            results[name] = get_pickle_hash(value, protocol)
        except (pickle.PickleError, TypeError) as e:
            results[name] = f"ERROR: {type(e).__name__}: {str(e)}"
    return results

def test_complex_structures(protocol=None):
    # these tests contains a bunch of more complex types.
    # Aswell as some nested stuff, like lists, dicts and mix of a bit of everything.
    # This is to see if everything is hashed correctly, and if the hash stays the same.
    tests = {
        "nested_list": [1, [2, 3], [4, [5, 6]]],
        "nested_dict": {"a": 1, "b": {"c": 2, "d": {"e": 3}}},
        "mixed_nested": {"name": "Test", "data": [1, 2, {"key": "value"}]},
        "tuple_with_various_types": (1, "string", 3.14, b"bytes", None),
        "set": {1, 2, 3, 4, 5},
        "frozenset": frozenset([1, 2, 3, 4, 5]),
        "namedtuple": Person(name="A Person", age=10, email="just@email.com"),
        "defaultdict": defaultdict(list, {"a": [1, 2], "b": [3, 4]}),
        "ordereddict": OrderedDict([("a", 1), ("b", 2), ("c", 3)]),
        "custom_object": CustomClass("test_object", 42),
        "datetime": datetime.datetime(2023, 1, 1, 12, 0, 0),
        "complex_mix": {
            "basic_types": [1, 2.0, "three", b"four", None, complex(5, 6)],
            "structured": {
                "tuple": (7, 8, 9),
                "set": {10, 11, 12},
                "custom": CustomClass("nested", 13),
                "timestamp": datetime.datetime(2023, 2, 3, 14, 15, 16)
            },
            "collection": [
                Person(name="Alice", age=25, email="alice@example.com"),
                Person(name="Bob", age=30, email="bob@example.com")
            ]
        }
    }

    results = {}
    for name, value in tests.items():
        try:
            results[name] = get_pickle_hash(value, protocol)
        except (pickle.PickleError, TypeError) as e:
            results[name] = f"ERROR: {type(e).__name__}: {str(e)}"

    return results


