import sys, os, pytest
from mpy import *

class Test_Types:
    def test_int(self):
        assert IntQ(1) == True

    def test_str(self):
        assert IntQ("1") == False

    def test_function(self):
        assert IntQ(1) == True

    def test_numeric(self):
        assert NumericQ <<Map>> [1, 3.14, "asdf", [1]] == [True,True, False, False]

class Test_StringQ:
    def test_str_1(self):
        assert StringQ(1) == False

    def test_str_2(self):
        assert StringQ("1") == True

    def test_str_3(self):
        assert StringQ([1,2,3]) == False

class Test_ListQ:
    def test_list_1(self):
        assert ListQ(1) == False

    def test_list_2(self):
        assert ListQ("1") == False

    def test_list_3(self):
        assert ListQ([]) == True

    def test_list_3(self):
        assert ListQ([1,2,[3]]) == True

class Test_FunctionQ:
    def test_function_1(self):
        assert FunctionQ(1) == False

    def test_function_2(self):
        assert FunctionQ("1") == False

    def test_function_3(self):
        assert FunctionQ([1]) == False

    def test_function_3(self):
        f = lambda x : x+1
        assert FunctionQ(f) == True


