# Motivation
Imagine you're writing a program to cook a meal; some burgers and steamed broccoli. Your first instinct is probably to cook them one at a time, like this:
```python
def main():
    get_pan()
    get_plates()
    get_buns()
    set_pan_on_burner()
    put_patties_on_pan()
    cook()
    steam_broccoli()
```
However, if you were to actually cook this meal, this isn't the procedure you would follow. You would probably start the broccoli steaming while the burger was still cooking. Your first instinct to translate this into a program might be to parallelize it:
```python
def make_burgers():
    get_pan()
    get_plates()
    get_buns()
    set_pan_on_burner()
    put_patties_on_pan()
    cook()

def main():
    p1 = Process(make_burgers)
    p2 = Process(steam_broccoli)
    p1.join()
    p2.join()
```

But this doesn't really match the way you'd do it in real life. After all, you don't need two people to cook this meal effeciently, do you? So why should you create two separate processes? 

# The solution: asynchronicity
So here's what this program should look something like:

```python
import asyncio

async def steam_brocolli():
    #Do brocolli stuff

async def cook():
    #Cook the borgers

async def main():
    brocolli_future = steam_broccoli()
    get_pan()
    get_plates()
    get_buns()
    set_pan_on_burner()
    put_patties_on_pan()
    await cook()
    await brocolli_future

if __name__ == "__main__":
    asyncio.run(main())
```
## The async keyword
So let's break down what this is doing. We can see that the functions main, cook, and steam_brocolli use a different kind of function signature. The async keyword indiciates that a function is asynchronous, meaning it does not need to be completed before proceeidng. If I were to translate it into English, it would be something like this: "You don't have to start this right now, but I want this done at some point." 

## The await keyword
On the last line, we see the new "await" keyword. What does that mean? It means that the program cannot proceed until this function is actually finished. However, it does <i>not</i> mean that this has to be done next. The program could decide to steam the broccoli first. If I were to translate await into English, it would say something like this: "You need to do this before we can move on. It's going to take awhile, so feel free to work on something else while it's running". Think back to the real-world example for a moment. If you were doing this in real life, you would probably start cooking the patties, then put the brocolli into the steamer and stick it in the microwave while the burgers are still cooking. 

## When should I use this?
This situation illustrates the the main use for asynchronous programming; <i>it is designed to minimize the time spent idly waiting for something outside the computer's control</i>. Cooking the burgers is going to take the same amount of time, regardless of what you're doing; it's a process that is outside your control. Crucially, <i>the burgers will continue to cook even if you stop watching them. Therefore, it is faster to do something else while they are cooking.</i> In a computer context, this would typically be a network request or reading from a file. Basically, async/await is useful when you're asking for information from the world outside your program, or sending that information to someone else. That's why the package is called async**io**, where IO is an abbreviation for input/output. 