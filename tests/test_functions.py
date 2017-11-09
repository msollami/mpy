import sys, os, pytest
from mpy import *

class Test_At:

    def test_at_1(self):
        f = lambda x: x+1
        assert At(f,1) == 2

    def test_at_2(self):
        f = lambda x: x * 2
        assert f <<At>> [1,2] == [1,2,1,2]


class Test_Apply:

    def test_apply_1(self):
        f = lambda x: x+1
        assert Apply(f,[1]) == 2

    def test_apply_2(self):
        f = lambda x,y: x+y
        assert Apply(f,(1,2)) == 3

class Test_Map:

    def test_map_1(self):
        f = lambda x: x+1
        assert Map(f,[1,2,3]) == [2,3,4]

    def test_map_2(self):
        f = lambda x: x+1
        assert Map(f,[]) == []

    def test_map_3(self):
        f = lambda x: x*2
        assert f <<Map>> [1,2,3] == [2,4,6]


