
# Introduction
Python is a dynamically typed language, which means that the type of a variable chan change whenever it is reassigned. This makes it tough for programs like VSCODE to do tab completion. However, if you use any decent IDE, you may have noticed that it manages anyway. How? There is a program known as *mypy* that IDE's use to guess at what the type of a value will be in a given line of code. This is why IDE's also tend to hog so much memory; they're doing this type checking all the time, which is expensive on large files. However, in many sitatutions, it is not possible to infer types automatically. Consider a function that can round a float to either  an int or a float. How could Mypy possibly infer the output of such a function? It can't. Not on its own, at least. This is where type hints come in.

# The typing module

## type
type() is a function that gets the type of an object. For example:
```
type(2)
<class 'int'>
```
## isinstance
isinstance is a built-in function in Python. It's purpose is fairly simple; it checks whether it's first argument is an *instance* of the second. for example: 
```
isinstance(2,int)
True
isinstance("2",int)
False
```
This allows you to do something like this:
```
def normalize(string):
    if isinstance(string,str)
        return string
    elif isinstance(string,bytes):
        return string.decode("utf-8")
type('1')
<class 'str'>
type(b'1')
<class 'bytes'>
type(normalize('1'))
<class 'str'>
type(normalize(b'1'))
<class 'bytes'>
```
    
# Basic type hint syntax
Type hint syntax is pretty simple. When you write a function like this:
```
def something(argument1, argument2):
    ...
```
The type hints would look something like this:
```
def something(argument1: int, argment2: str)->int:
    ...
```
This indicates that argument1 should be an integer, argument2 should be a string, and the output will be an integer.

## Caveat
One thing to note about type hints is that Python itself pretty much completely ignores them. If you were to call the function above like this:
```
something("1",2)
```
Python wouldn't object. If you're using a decent code editor like VSCODE, it'll warn you with Mypy, but Python won't do that on its own.

# Custom types
Type hints can be any primitive type, like int or str, but they can also be any kind of Python class, including ones that you write. Sometimes, because Python's typing system is *great*, it likes to complain sometimes for no good reason. For example, if you do this:
```
class test():
    def method(self)->test:
```
Python will refuse to run the program. When this happens, do this instead:
```
class test():
    def method(self)->"test"
```
and the problem will stop. Honestly, it's not a terrible idea to always wrap your hints in quotes. You might be wondering why Python crashes at an """undefined""" type if it ignores them. Me too. Anyway...

# More advanced types
Python's typing module contains some more advanced types, like lists and sets. They look like this:
```
import typing

def listSomething(argument1: int, argument2: str)->typing.List[int]
```
See the square brackets after List? That's called a *type parameter*. In this case, it indicates that the output is not just a list of anything you want, but specifically a list of integers. In most programming languages, this is done with the '\<' and '\>' symbols, but Python decided to break that mold, for no apparent reason. 

## Union types
the typing module has a very useful type called typing.Union. It allows the input to be one of several types. Let's use it to add type hints to our normalize function from eariler:
```
def normalize(string: typing.Union[str,bytes])->str:
    ...
```
In 3.10 and above, you could also do this:
```
def normalize(string: str|bytes)->str:
    ...
```
Note that because Python is strangely whiny about type hints it ultimately ignores, if you use a version before 3.10 and use the | syntax, Python will crash.
## Caveat
Note that these generic types *will not work with isinstance!* Furthermore, type(\[1,2,3\]) will not include the \[int\] part. The part in brackets is for *humans only!*

# Type variables
Now that you know about generic types, you're ready for type variables. Let's say we have a function that does division, and it returns a float if the parameters are floats, or ints if they are integers. How would we express that with type hints? here's how:
```
import typing
T = typing.TypeVar("T")
def some_math(param1: T, param2: T)->T:
    ...
```
This type variable takes on the type of the parameters (we're implicitly assuming they match), and sets the output type of the function accordingly. So the output type of some_math(2,3) is int, but the output type of some_math(2.5,3.5) is float, despite them being the exact same function. Note that this is *not* the same as a union type! If it were a union type, the output type of both of those examples would be int
|float, and you wouldn't necessarily know which one it was.

## Basic constraints
 We can also put constraints on what values T can be:
```
T = typing.TypeVar("T",int,float)
```
Now T must be either type int or type float.

## (Slightly) more advanced constraints
Take these two classes:
```
class Test():
    x: int

class Tester(Test):
    y: int
```
If you were to do this:
```
T = typing.TypeVar("T",Test)
def test(t: T)->T:
    ...
test(Tester())
```
this is considered invalid, because the type of Tester() does not exactly match Test. You'd want this instead:
```
T = typing.TypeVar("T",bound=Test)
```

# Overloads
Remember these from C++? Turns out python has them too. Sort of. Not really. Here's an example. Suppose we have a function called rounder, that takes an optional parameter digits. If digits is not supplied, it returns an integer. If it is, it returns a float rounded to that number of digits. With what we've learned so far, it is not possible to correctly type this function. You need overloads to do this:
```
import typing

@typing.overload
def rounder(x: float)->int:
    pass
@typing.overload
def rounder(x: float, digits: int)->float:
    pass
def rounder(x: float, digits: int = 0)->int|float:
    ...
```
There are a few rules you need to keep in mind when using overloads. <br/>
Number one: Python ignores them, because of course it does. They are for humans and IDE's only. <br/>
Number two: The *last* declaration is the one Python will use. <br/>
Number three: if python tries to call a function with @typing.overload over it, it will crash. <br/>
Adding type hints to the last declaration will have no effect on the type checker outside the function, but I prefer to do it anyway for consistency's sake.

## Challenge
Here's a small puzzle for you. The typing of this overloaded function is actually not *quite* right. If you do this:
```
x = rounder(1.2,0)
```
mypy thinks x should be a float, but it's actually an integer! You can see this in Vs code by copy-pasting the functions into a code editor and hovering over x to view its type. I want you to leaf through <a href=https://docs.python.org/3/library/typing.html#special-typing-primitives>this page</a> and try to fix this on your own. My solution used just one extra overload. Here's a hint: the order of the overloads matters!