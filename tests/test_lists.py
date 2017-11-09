import sys, os, pytest
from mpy import *

class Test_Lists:

    def test_take(self):
        assert Take([1,2,3],1) == [1]
        assert Take([1,2,3],2) == [1,2]
        assert Take([1,2,3],-1) == [3]
        assert Take([1,2,3],-3) == [1,2,3]
        assert Take([1,2,3,4,5,6], [2,4]) == [2,3,4]
        assert Take(["a", "b", "c", "d", "e", "f"], [2]) == ["b"]

        assert Take({5:"a", 6:"b", 7:"c"}, 2) == {5:"a", 6:"b"}
        assert Take({5:"a", 6:"b", 7:"c"}, -2) == {6:"b", 7:"c"}
        assert Take({5:"a", 6:"b", 7:"c"}, [2]) == {6:"b"}

        # assert Take[(1,2,3,4), 2] == (1,2)


#    def test_rest(self):
#        assert Rest([1,2,3]) == [2,3]
#
#    def test_most(self):
#        assert Most([1,2,3]) == [1,2]
#
#        with pytest.raises(TypeError):
#            Most(2)
#
#        with pytest.raises(TypeError):
#            Most("string")

    def test_dimensions(self):
        assert Dimensions([[1, 2, 3], [1, 2, 3]]) == [2,3]
        assert Dimensions([[1, 2, 3], [1,2], [1]]) == [3]
        assert Dimensions([[[["a", "b"]]]]) == [1,1,1,2]
        assert Dimensions([[[["a", "b"]]]], 2) == [1, 1]


#    def test_range(self):
#        assert Range(10,1,-1) == [10,9,8,7,6,5,4,3,2,1]

#     def test_table(self):
#         assert self.M.table(1, 6) == [1,1,1,1,1,1]
#         g = lambda x: x**2
#         assert self.M.table(g, 10) == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
#         assert self.M.table(1, (3,3)) == [[1,1,1],[1,1,1],[1,1,1]]
#         assert self.M.table(1,('i',10)) == [[1,1,1],[1,1,1],[1,1,1]]


