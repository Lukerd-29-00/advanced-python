# Sessions
Today we're going to learn how to do network requests a bit more efficiently in Python.

## Test
The first thing I want you to do is a quick experiment. google "internet speed test" and note your internet download speed, then download and run slow.py.

### Results
You probably noticed that the download speed in slow.py is, well, slow. For me, my download speed can be as good as 20 MB/s, but for this script I got about 60 KB. Why this huge difference? Your first guess might be that the website you're downloading from is slower than that (which is true, actually). However, if you run fast.py, you should notice a marked speed increase. I got about 150 KB/s, which is almost triple the speed!

## Why is fast.py faster?
If you haven't already, take a look at the code between the two scripts. You'll notice that the code is fairly similar. In fact, the code that downloads the website is identical, with one difference. Slow.py uses requests.get, while fast.py is wrapped in the requests.Session class and uses its .get method instead.

## What is a session, exactly?
When you open a connection to a website, you can't just start downloading right away. Computers do a sort of handshake when they open a new connection, which takes a couple of round trips before you can start the actual download. The difference between these scripts is that slow.py does this handshake for *every single downloaded pokemon*, while fast.py starts the connection *once*. This is why sessions are so important; even if you're only making two or three requests, they will pretty much always be faster.

# Closing notes
 I want to draw your attention to the absolute amount of time the scripts take. Notice that there is a difference of several seconds, even for operating on just a few hundred Kilobytes. If you were to try to optimize a program like this by, say, using a more efficient sorting algorithm or something, you would probably be saving nanoseconds if you were lucky. If you take anything away from this, it's this; *networking is the bottleneck in basically every program that uses it!* For data sets this small, using a better algorithm for a computational task is might not even worth the storage space the code takes up, let alone the development time. But network efficiency can turn a ten second task into a three second one, or even less.