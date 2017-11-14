# coding=utf-8
import os, glob
import numpy as np
from infix import shift_infix as infix
from collections import OrderedDict

"""
Base mma-like functions.
"""


# ===============================================================================
# Types
# ===============================================================================

def BooleanQ(obj):
    return obj is True or obj is False


def TrueQ(obj):
    return obj is True


def FalseQ(obj):
    return obj is False


def IntQ(obj):
    return isinstance(obj, int)


def ListQ(obj):
    return isinstance(obj, list)


def AssociationQ(obj):
    return isinstance(obj, dict)


def FunctionQ(obj):
    return hasattr(obj, '__call__')


def StringQ(obj):
    return isinstance(obj, basestring)


def TupleQ(obj):
    return type(obj) == tuple


def NumericQ(obj):
    return isinstance(obj, int) or isinstance(obj, float)


# ===============================================================================
# Logic
# ===============================================================================

def And(*args):
    """
    And(e1, e2, ...) is the logical AND function.

    It evaluates its arguments in order, giving False immediately if any of them are False, and True if they are all True.

    :param args:
    :return:
    """
    """
    :param args:
    :return:
    """
    li = list(args)

    check = [BooleanQ(v) for v in li]

    if False in check:
        raise TypeError

    if False in li:
        return False
    elif True in li:
        return True

    return li


def Or(*args):
    """
    Or[e1, e2, ...] is the logical OR function.

    It evaluates its arguments in order, giving True immediately if any of them are True, and False if they are all False.

    :param args:
    :return:
    """
    li = list(args)

    check = [BooleanQ(v) for v in li]

    if False in check:
        raise TypeError

    if True in li:
        return True
    elif False in li:
        return False

    return li



# ===============================================================================
# Files
# ===============================================================================



def FileNames(dir_string=os.path.abspath(os.getcwd())):
    return glob.glob(dir_string)



# ===============================================================================
# Lists
# ===============================================================================

def Part(li, spec):
    """
    Part[expr,i] gives the i^th part of expr.
    expr[[-i]] counts from the end.
    expr[[i,j,\[Ellipsis]]] or Part[expr,i,j,\[Ellipsis]] is equivalent to expr[[i]][[j]]\[Ellipsis].
    expr[[{Subscript[i, 1],Subscript[i, 2],\[Ellipsis]}]] gives a list of the parts Subscript[i, 1], Subscript[i, 2], \[Ellipsis] of expr.
    expr[[m;;n]] gives parts m through n.
    expr[[m;;n;;s]] gives parts m through n in steps of s.
    expr[["key"]] gives the value associated with the key "key" in an association expr.
    expr[[Key[k]]] gives the value associated with an arbitrary key k in the association expr.

    :param li:
    :param spec:
    :return:
    """


def Take(li, n):
    """
    Take[list,n] gives the first n elements of list.
    Take[list,-n] gives the last n elements of list.
    Take[list,{m,n}] gives elements m through n of list.
    Take[list, seq1, seq2,...] gives a nested list in which elements specified by seqi are taken at level i in list.


    :param li:
    :param n:
    :return:
    """
    if not ListQ(li) and not AssociationQ(li):
        raise TypeError("Argument expected to be list.")

    if ListQ(li):
        if IntQ(n):
            if n > 0:
                return list(li[0:n])
            else:
                return list(li[n + len(li):])

        elif ListQ(n) or TupleQ(n):
            if len(n) == 1:
                if n[0] > 0:
                    return [li[n[0] - 1]]
                else:
                    return [li[n[0]]]

            if len(n) == 2 and n[0] > 0 and n[1] > 0:
                return list(li)[n[0] - 1:n[1]]
            else:
                raise ValueError

    elif AssociationQ(li):
        # d = OrderedDict();
        # d['equals'] = String.equals
        # d['contains'] = String.contains

        items = li.items()

        if IntQ(n):
            if n > 0:
                return dict(Take(items, n))
            else:
                return dict(items[n + len(items):])

        elif ListQ(n) or TupleQ(n):

            return dict(Take(items, n))

    return {}


def Dimensions(l, level=None):
    """
    Dimensions[expr] gives a list of the dimensions of expr.
    Dimensions[expr,n] gives a list of the dimensions of expr down to level n.


    """
    if not ListQ(l):
        raise TypeError("Not a list")

    if level:
        if IntQ(level) and level > 0:
            return Take(list(np.shape(l)), level)
        else:
            raise TypeError("Bad level.")
    else:
        return list(np.shape(l))


def Table(expr, spec):
    """
    Table(expr,n) generates a list of n copies of expr.
    Table(expr,{i, imax}] generates a list of the values of expr when i runs from 1 to Subscript[i, max].
    Table[expr,{i,imin,imax}] starts with i=imin.
    Table[expr,{i,imin,imax,di}] uses steps di.
    Table[expr,{i,{i1,i2,...}}] uses the successive values i1, i2, ....
    Table[expr,{i,Subscript[i, min],Subscript[i, max]},{j,Subscript[j, min],Subscript[j, max]},...] gives a nested list.
    The list associated with i is outermost.

    """

    if IntQ(spec):
        return ([expr] * spec)
    elif ListQ(spec):
        return ([expr] * spec)
    elif FunctionQ(expr) and TupleQ(spec):
        pass
    else:
        raise TypeError("e")


def Range(min, max=None, step=None):
    """
    Range(max) generates the list [1,2,.. ,max].
    Range(min, max) generates the list [min, ..., max].
    Range(min, max, di) uses step di.
    :param step:

    """
    if not max and not step:
        return np.arange(1, min + 1)

    elif NumericQ(min) and NumericQ(max) and not step:
        return np.arange(min, max + 1)

    elif Apply(And, NumericQ << Map >> [min, max, step]):
        if step > 0:
            return np.arange(min, max + 1, step)
        else:
            return np.arange(min, max - 1, step)


# ===============================================================================
# Functional Programming
# ===============================================================================

@infix
def At(a, b):
    if not FunctionQ(a):
        raise TypeError("Not a function")
    return a(b)


@infix
def Apply(f, b):
    """
    Apply[f,expr] replaces the head of expr by f.
    Apply[f,expr,{1}] replaces heads at level 1 of expr by f.
    Apply[f,expr,levelspec] replaces heads in parts of expr specified by levelspec.
    Apply[f] represents an operator form of Apply that can be applied to an expression.

    :param f:
    :param b:
    :return:
    """
    if not FunctionQ(f):
        raise TypeError("Not a function")
    else:
        return f(*tuple(b))


@infix
def Map(f, b):
    """
    Map[f,expr] applies f to each element on the first level in expr.
    Map[f,expr,levelspec] applies f to parts of expr specified by levelspec.
    Map[f] represents an operator form of Map that can be applied to an expression.

    :param f:
    :param b:
    :return:
    """
    if not FunctionQ(f):
        raise TypeError("Not a function")

    if not ListQ(b):
        raise TypeError("Not a list")

    return map(f, b)

#===============================================================================
# IO
#===============================================================================

@infix
def FileExistsQ(fname):
    """
    FileExistsQ("name") gives True if the file with the specified name exists, and gives False otherwise.

    :param f: file
    :return: boolean type

    """

    import os.path
    return os.path.isfile(fname) 


@infix
def Import(f):
    """
    Import("file") imports data from a file.
    Import("file",elements) imports the specified elements from a file.
    Import("http://url", ...) and Import("ftp://url", ...) import from any accessible URL.

    :param f: file
    :return: contents of file

    """
    import json

    if not FileExistsQ(f):
        raise ValueError("Not a file")

    res = None
    filename, file_extension = os.path.splitext(f)
    
    if file_extension == '.json':
        with open('strings.json') as json_data:
            res = json.load(json_data)
    else:
        raise ValueError("Filetype not supported")

    return res

def Export(filename, data, overwrite=False):
    """
    """
    if not overwrite:
        if FileExistsQ(filename):
            raise ValueError("Target file exists.")
    
    if isinstance(data, basestring):
        with open(filename, 'wb') as f:
            f.write(data)
    elif isinstance(data, dict):
        import json
        with open(filename, 'wb') as f:
            json.dump(data, f)
    
    return filename


#
# MapIndexed - map with index information: {f[x,{1}],f[y,{2}],f[z,{3}]}
#
# MapThread  MapAt  MapAll  Scan  ...
#
# Iteratively Applying Functions »
#
# Nest, NestList, NestGraph - nest a function: f[f[f[x]]] etc.
#
# Fold, FoldList - fold in a list of values: f[f[f[x,1],2],3] etc.
#
# SequenceFold  SequenceFoldList  FoldPair  FoldPairList
#
# FixedPoint, FixedPointList - repeatedly nest until a fixed point
#
# NestWhile  NestWhileList  TakeWhile  LengthWhile  ...
#
#
#
# List-Oriented Functions »
#
# Select - select from a list according to a function
#
# Array - create an array from a function
#
# SortBy  MaximalBy  SplitBy  GatherBy  ...
#
# Association-Oriented Functions
#
# AssociationMap - create an association from a function
#
# KeySortBy  CountsBy  GroupBy  ...
#
#
#
# Functional Composition
#
# Identity  Composition  Operate  Through  Distribute  ...
#
# "Curried" Operator Forms
#
# Select  Cases  Append  Map  Position  ...
# """
#
#
# #===============================================================================
# # Procedural Programming
# #===============================================================================
#
# """
# x=value  (Set)- set the value for a variable
#
# expr;expr;expr  (CompoundExpression)- execute expressions in sequence
#
#
#
# Assignments »
#
# =  +=  ++  *=  AppendTo  ...
#
# Loops »
#
# Do  While  For  Table  Nest  ...
#
# Conditionals »
#
# If  Which  Switch  And(&&)  Equal(==)  Less(<)  ...
#
# Flow Control »
#
# Return  Throw  Catch  TimeConstrained  ...
#
# Scoping Constructs »
#
# Module  With  Block  ...
#
# Input, Output, Etc. »
#
# Print  Input  Pause  Import  OpenRead  ...
#
# """
#
#
# #===============================================================================
# # Basic Math
# #===============================================================================
#
#
# """
# Association ( <|\[Ellipsis]|> )- an association between keys and values
#
# <|\[Ellipsis]|>[key]- extract the value associated with any given key
#
# Associations and Parts
#
# <|\[Ellipsis]|>[["str"]]- extract a value corresponding to a key that is a string
#
# Key- indicate a key within a part specification
#
# Missing- default value if a key is not found
#
# #name- a slot in a pure function that picks out value with key "name" in an association
#
# AssociationQ- test if an expression is a valid association
#
#
#
# Elements of Associations
#
# Keys- list of keys
#
# Values- list of values
#
# Normal- convert to a list of rules
#
# Lookup- perform a lookup of a value by key, returning a specified default if it is not found
#
# KeyExistsQ- test whether a key exists in an association
#
#
#
# Functions That Apply to Values »
#
# Map  Select  Sort  DeleteDuplicates  ListPlot  Plus  ...
#
# Functions That Apply to Keys
#
# KeySort, KeySortBy- sort an association by its keys
#
# KeyTake, KeyDrop- take, drop particular keys in an association
#
# KeySelect- select elements based on a criterion on their keys
#
# KeyMap- map a function over the keys in an association
#
# KeyValueMap- map a function over keys and values in an association
#
# Modifying Associations
#
# <|\[Ellipsis]|>[key]=val- change an element of an association
#
# AssociateTo- add elements to an association
#
# KeyDropFrom- drop elements from an association
#
#
#
# Functions That Create Associations
#
# Association- turn a list of rules into an association
#
# AssociationMap- create an association by applying a function to a list of keys
#
# AssociationThread- create an association from a list of keys and a list of values
#
# Counts, CountsBy- associate values with the number of times they occur
#
# GroupBy- group values by collecting those sharing a criterion ("map reduce")
#
# PositionIndex- build an index of positions at which values occur
#
# Functions Operating on Lists of Associations
#
# KeyUnion  KeyIntersection  KeyComplement
#
# Catenate- catenate elements from multiple associations
#
# Merge- merge associations using a function to combine elements with common keys
#
# JoinAcross- do the analog of a database join on multiple associations
#
# Dataset- representation supporting general structured data queries
#
#
# """
#
#
# #===============================================================================
# # Basic Math
# #===============================================================================
#
# global E
# E = np.e
# """
# E is the exponential constant E (base of natural logarithms), with numerical value \[TildeEqual]2.71828.
# """
#
# global Pi
# Pi = np.pi
# """
# Pi  is \[Pi], with numerical value \[TildeEqual]3.14159.
# """
#
# def Power(x,y):
#     """
#     x^y gives x to the power y.
#
#     :param x:
#     :param y:
#     :return:
#     """
#     pass
#
# def Exp(z):
#     """
#     Exp[z] gives the exponential of z.
#     :param z:
#     :return:
#     """
#
# def Sqrt(x):
#     """
#     Sqrt[z] gives the square root of z.
#     :param x:
#     :return:
#     """
#
#     pass
#
# def Total(li):
#     """
#     Total[list] gives the total of the elements in list.
#     Total[list,n] totals all elements down to level n.
#     Total[list,{n}] totals elements at level n.
#     Total[list,{n1, n2}] totals elements at levels n1 through n2.
#
#
#     :param li:
#     :return:
#     """
#     pass
#
#
# def Accumulate(li):
#     """
#     Accumulate[list] gives a list of the successive accumulated totals of elements in list.
#
#     :param li:
#     :return:
#     """
#     pass
#
#
#
#
# def Differences(li):
#     """
# 	Differences[list] gives the successive differences of elements in list.
# 	Differences[list,n] gives the n\[Null]^th differences of list.
# 	Differences[list,n,s] gives the differences of elements step s apart.
# 	Differences[list,{Subscript[n, 1],Subscript[n, 2],\[Ellipsis]}] gives the successive Subscript[n, k]\[Null]^th differences at level k in a nested list.
#
#
#
#     :param li:
#     :return:
#     """
#     pass
#
#
#
# #===============================================================================
# # Expressions
# #===============================================================================
# def Head(expr):
#     """
#     Head[expr] gives the head of expr.
#
#     :param expr:
#     :return:
#     """
#     pass
#
# def Fullform(expr):
#     """
#
#     FullForm[expr] prints as the full form of expr, with no special syntax.
#
#     :param expr:
#     :return:
#     """
#     pass
#
#
# def TreeForm(expr):
#     """
#     TreeForm[expr] displays expr as a tree with different levels at different depths.
#     TreeForm[expr,n] displays expr as a tree only down to level n.
#
#
#     :param expr:
#     :return:
#     """
#
# def Level(expr, spec):
#     """
# 	Level[expr,levelspec] gives a list of all subexpressions of expr on levels specified by levelspec.
# 	Level[expr,levelspec,f] applies f to the sequence of subexpressions.
#
#
#     """
#     pass
#
# def Depth(expr):
#     """
#     Depth[expr] gives the maximum number of indices needed to specify any part of expr, plus 1.
#     """
#     pass
#
#
#
# def ByteCount(expr):
#     """
#     ByteCount[expr] gives the number of bytes used internally by the Wolfram System to store expr.
#     """
#     pass
#
#
#
#
# #===============================================================================
# # Sugar
# #===============================================================================
#
# def Length(expr):
#     """
#     Length[expr] gives the number of elements in expr.
#     """
#     pass
#
#
# def First(li):
#     """
#
#     """
#
#     if not ListQ(li):
#         raise TypeError("Argument expected to be list.")
#
#     return li[0]
#
# def Last(li):
#     """
#
#     """
#     if not ListQ(list):
#         raise TypeError("Argument expected to be list.")
#
#     return list[len(li)]
#
#
#
# #===============================================================================
# # Handling Arrays of Data
# #===============================================================================
# """
# Ratios  Fold
#
# Max  Min  MinMax  Commonest  Sort  SortBy  Ordering
#
# TakeLargest  TakeSmallest  TakeLargestBy  TakeSmallestBy
#
# MaximalBy, MinimalBy - maximal, minimal elements based on a criterion
#
# Union 
# Position
# Count
# Counts 
# BinCounts - count the number of elements in a sequence of bins
# CountDistinct - count the number of distinct elements
# CountDistinctBy - count distinct values from applying a function
# """
#
# #===============================================================================
# # Core Language - Symbols
# #===============================================================================
# """
# Attributes
# SetAttributes 
# ClearAttributes
#
# x=\[Ellipsis] - set a variable
#
# f[x_]:=\[Ellipsis] - define a function that takes any single argument
#
#
#
# Assignments »
#
# Set (=) - immediate assignment (right-hand side evaluated immediately)
#
# SetDelayed (:=) - delayed assignment (right-hand side evaluated only when used)
#
# Unset (=.) - unset a variable
#
# Clear - clear a function definition
#
#
#
# Function Argument Patterns »
#
# __(BlankSequence)  p|p(Alternatives)  p:e (Optional)
#
# Bodies of Functions »
#
# Module, ... - scope local variables
#
# e;e;e (CompoundExpression) - execute expressions in sequence
#
# Function Attributes »
#
# Attributes  Flat  Orderless  Listable  HoldFirst  Protected
#
#
# Setting Up Options for Functions
# SetOptions - set up default option values for a function
# OptionsPattern - a pattern representing an arbitrary sequence of options
# OptionValue - retrieve values of options while executing a function
# FilterRules - filter particular options from a longer list
#
# Options - get the options for a function or object with options
# AbsoluteOptions - get explicit values for options that are given as Automatic, etc.
# """
# #===============================================================================
# # Strings
# #===============================================================================
#
# """
# Structural Operations
# StringJoin (<>) - join strings together
# StringLength - length of a string
# StringSplit - split a string at spaces or other delimiters
# StringTake, StringDrop - take or drop parts of a string
# String Patterns »
# StringExpression - a symbolic string expression including symbolic string patterns
# Longest  Shortest  Except  Whitespace  NumberString  ...
#
# Operations on Strings »
# StringReplace - make replacements for string patterns
# StringCases - find cases of string patterns
# StringContainsQ - test whether a string contains a string pattern
# StringCount  StringPosition  StringRepeat  StringDelete  ...
# Sort - sort lists of strings alphabetically or otherwise
#
# String Templating »
# StringTemplate - create a string template
# <*\[Ellipsis]*> - expression for evaluation within a string template
# `\[Ellipsis]` - slot for substitution
# TemplateApply  FileTemplateApply  ...
# Text Construction
# StringRiffle  StringPadLeft  Pluralize  ...
#
# Character-Oriented Operations »
# Characters - break a string into a list of characters
# ToUpperCase  ToCharacterCode  LetterQ  Alphabet  ...
#
# String Alignment & Comparison »
# SequenceAlignment - find matching sequences in strings
# Nearest - find strings nearest in edit distance
# HammingDistance  EditDistance  LongestCommonSubsequence  ...
# String Analysis »
# CharacterCounts  TextWords  DictionaryLookup  WordCloud  ...
#
# String Semantics
# ToString, ToExpression - convert between expressions and strings
# Interpreter - interpret strings according to many type specifications
# SemanticInterpretation - interpret strings semantically
# ImportString, ExportString - translate strings in many file and other formats
# "XML"  "Table"  ...
# TextString - give a textual version of any expression as a string
#
# Systems-Related Operations »
# Hash  StringForm  Compress  Encrypt  ...
# Operations on File Names »
# FileNameSplit  FileNameTake  FileBaseName  ExpandFileName  ...
# Operations on URLs »
# URLEncode  URLDecode  URLBuild  URLParse  ...
#
#
#
# Text Normalization »
#
# ToLowerCase  ToUpperCase  RemoveDiacritics  CharacterEncoding  ...
#
# DeleteStopwords - delete standard stopwords ("the", "and", etc.) from a string
#
# StringSplit - split a string at newlines or other delimiters
#
# StringReplace  StringDelete  StringTrim  ...
#
# Structural Text Manipulation
#
# TextCases - extract symbolically specified elements
#
# TextSentences - extract a list of sentences
#
# TextWords - extract a list of words
#
# SequenceAlignment - find matching sequences in text
#
# Searching & Pattern Matching »
#
# StringExpression - general string pattern
#
# StringMatchQ  StringCases  StringCount  ...
#
#
#
# Text Analysis »
#
# WordCounts - count occurrences of words and n-grams
#
# LetterCounts  CharacterCounts  WordCount
# """
#
#
# #===============================================================================
# # Data Plotting
# #===============================================================================
#
# """
# ListPlot- plot lists of points
#
# ListLinePlot- plot lines through lists of points
#
# ListStepPlot- plots values in steps
#
# ListLogPlot  ListLogLinearPlot  ListLogLogPlot  ListPolarPlot
#
#
#
# ListPlot3D- 3D plot from lists of 3D height data
#
# ListPointPlot3D- 3D point scatter plot
#
#
#
# ListDensityPlot,ListDensityPlot3D- color density plots from 3D and 4D height data
#
# ListContourPlot, ListContourPlot3D- iso contour plots from 3D and 4D height data
#
#
#
# ListSliceDensityPlot3D- color densities on surface slices through 4D height data
#
# ListSliceContourPlot3D- contour shading on surface slices through 4D height data
#
#
#
# ListCurvePathPlot, ListSurfacePlot3D- reconstruct curves and surfaces from points
#
#
#
# ArrayPlot- plot an array of values or colors
#
# ReliefPlot- plot an array with simulated relief
#
# MatrixPlot- plot values in a matrix
#
#
#
# Temporal Visualization
#
# DateListPlot, DateListLogPlot- date and time plots
#
# TimelinePlot- timeline allowing labeling
#
# DateHistogram- histogram of dates or times
#
#
#
# Vector Visualization »
#
# ListStreamPlot  ListStreamDensityPlot  ListVectorPlot  ListVectorPlot3D  ...
#
#
#
# Graph Visualization »
#
# GraphPlot- lay out a general graph
#
# LayeredGraphPlot- draw a graph in a layered or hierarchical way
#
# TreePlot- draw a tree structure
#
#
#
# Charting & Information Visualization »
#
# BarChart  PieChart  BubbleChart  BarChart3D  ...
#
# Statistical Visualization »
#
# Histogram  Histogram3D  QuantilePlot  BoxWhiskerChart  ...
#
# Gauges »
#
# AngularGauge  HorizontalGauge  VerticalGauge  ...
#
#
#
# Visualization of Tabular Data »
#
# Grid  Row  Column  Multicolumn  GraphicsGrid  GraphicsRow  ...
#
# Collective Data Visualization
#
# WordCloud  ImageCollage  ImageAssemble
#
#
#
# Geographic Visualization »
#
# GeoGraphics  GeoPath  Entity  ...
#
#
#
# Interval Visualization
#
# NumberLinePlot- plot points and intervals on the number line
#
# Discrete Function Visualization »
#
# DiscretePlot- plot functions f(n) of a discrete variable
#
# Wavelet Visualization »
#
# WaveletScalogram  WaveletListPlot  WaveletMatrixPlot  ...
#
#
#
# Styling Options »
#
# Frame  PlotStyle  Filling  Mesh  ImageSize  ...
#
# Legends »
#
# PlotLegends  Legended  LineLegend  BarLegend  ...
