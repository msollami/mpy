import numpy as np
import collections


def column(df, n):
    """

    :param f:
    :param df:
    :param n:
    :return:
    """
    col = df[df.columns[n]]
    col = map(f, col)
    df[df.columns[n]] = col


def map_col(f, df, n):
    """

    :param f:
    :param df:
    :param n:
    :return:
    """
    col = df[df.columns[n]]
    col = map(f, col)
    df[df.columns[n]] = col


def Join(matrix, i):
    pass


def column(matrix, i):
    pass #return [row[i] for row in matrix]


def most_common(lst, n=1):
    c = collections.Counter(lst)
    mc = c.most_common(n)
    if n == 1:
        return mc[0][0]
    else:
        return [m[0] for m in mc]

def positions(m, val):
    pos = []
    for i, x in enumerate(m):
        for j, y in enumerate(x):
            if y == val:
                pos.append([i, j])
    return np.array(pos)


def diskMatrix(r=3):
    n = 2 * r + 1
    a, b = n / 2.0, n / 2.0

    print n, a, b

    y, x = np.ogrid[-a:n - a, -b:n - b]
    mask = x * x + y * y <= r * r
    array = np.zeros((n, n))
    array[mask] = 1
    return array


def rotate_left(arr, n):

    print "types = ", type(arr), type(n)

    if not type(arr) is list:
        arr = arr.tolist()
        #raise ValueError("arr is %s, should be a list!" % str(type(arr)))

    if type(arr) is np.ndarray:
        arr = arr.tolist()

    if type(n) is np.ndarray:
        n = n.tolist()

    if type(n) is int:
        d = collections.deque(arr)
        d.rotate(-n)
        d = list(d)
        return d

    elif type(n) is list:
        #rotate both levels
        d = collections.deque(arr)
        d.rotate(-n[0])

        if len(n) == 2:
            d = list(d)
            d = map(lambda x: rotate_left(x, n[1]), d)

        d = list(d)
        return d



# def column(obj, n):
#
#     if type(obj) == ".sdf":
#         return obj[obj.columns[0]
