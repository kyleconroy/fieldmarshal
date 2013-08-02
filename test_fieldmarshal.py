from fieldmarshal import Struct
import fieldmarshal
import json
from nose.tools import assert_equals


class Foo(Struct):
    id = str


class Bar(Struct):
    id = bool


class Baz(Struct):
    id = int


class Bap(Struct):
    id = None


class Nested(Struct):
    foo = Foo

class SuperNested(Struct):
    nested = Nested


def test_recursive_dumps():
    c = Nested(foo = Foo(id = "foo"))
    assert_equals(fieldmarshal.dumps(c), json.dumps({"foo": {"id": "foo"}}))


def test_recursive_load():
    resp = json.dumps({"foo": {"id": "foo"}})
    c = fieldmarshal.loads(Nested, resp)
    assert_equals(c.foo.id, "foo")


def test_deeper_load():
    resp = json.dumps({"nested": {"foo": {"id": "foo"}}})
    c = fieldmarshal.loads(SuperNested, resp)
    assert_equals(c.nested.foo.id, "foo")


def test_dumps():
    c = Foo(id = "foo")
    assert_equals(fieldmarshal.dumps(c), json.dumps({"id": "foo"}))


def test_zero_value_string():
    c = Foo()
    assert_equals(c.id, "")


def test_zero_value_none():
    c = Bap()
    assert_equals(c.id, None)


def test_zero_value_bool():
    c = Bar()
    assert_equals(c.id, False)


def test_zero_value_int():
    c = Baz()
    assert_equals(c.id, 0)


def test_zero_value_struct():
    c = Nested()
    assert_equals(c.foo.id, "")


def test_loads():
    resp = json.dumps({"id": "foo"})
    c = fieldmarshal.loads(Foo, resp)
    assert_equals(c.id, "foo")
