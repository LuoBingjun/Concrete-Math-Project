# Eel
Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps, with full access to Python capabilities and libraries.

**It hosts a local webserver, then lets you annotate functions in Python so that they can be called from Javascript, and vice versa.**

It is designed to take the hassle out of writing short and simple GUI applications. If you are familiar with Python and web development, probably just jump to [this example](https://github.com/ChrisKnott/Eel/tree/master/examples/04%20-%20file_access) which picks random file names out of the given folder (something that is impossible from a browser).

<p align="center"><img src="examples/04%20-%20file_access/Screenshot.png" ></p>

### Intro

There are several options for making GUI apps in Python, but if you want to use HTML/JS (in order to use jQueryUI or Bootstrap, for example) then you generally have to write a lot of boilerplate code to communicate from the Client (Javascript) side to the Server (Python) side.

The closest Python equivalent to Electron (to my knowledge) is [cefpython](https://github.com/cztomczak/cefpython). It is a bit heavy weight for what I wanted.

Eel is not as fully-fledged as Electron or cefpython - it is probably not suitable for making full blown applications like Atom - but it is very suitable for making the GUI equivalent of little utility scripts that you use internally in your team. 

For some reason many of the best-in-class number crunching and maths libraries are in Python (Tensorflow, Numpy, Scipy etc) but many of the best visualation libraries are in Javascript (D3, THREE.js etc). Hopefully Eel makes it easy to combine these into simple utility apps for assisting your development.

### Install

Install from pypi with `pip`:

    pip install eel

### Usage

#### Structure

An Eel application will be split into a frontend consisting of various web-technology files (.html, .js, .css) and a backend consisting of various Python scripts.

All the frontend files should be put in a single directory (they can be further divided into folders inside this if necessary).

```
my_python_script.py     <-- Python scripts
other_python_module.py
static_web_folder/      <-- Web folder
  main_page.html
  css/
    style.css
  img/
    logo.png
```

#### Starting the app

Suppose you put all the frontend files in a directory called `web`, including your start page `main.html`, then the app is started like this;

```python
import eel
eel.init('web')
eel.start('main.html')
```

This will start a webserver on the default settings (http://localhost:8000) and open a browser to http://localhost:8000/main.html.

If Chrome or Chromium is installed then by default it will open in that in App Mode (with the `--app` cmdline flag), regardless of what the OS's default browser is set to (it is possible to override this behaviour).

#### App options

Additional options can be passed to `eel.start()` by passing it an `options={}` argument.

Some of the options include the mode the app is in ('chrome', 'chrome-app', None), the port the app runs on, the host name of the app, and adding additional Chrome/Chromium command line flags.

The defaults are set to:
```
_default_options = {
    'mode': 'chrome-app',
    'host': 'localhost',
    'port': 8000,
    'chromeFlags': ""
}
```

##### Chrome/Chromium flags
You can add additional Chrome/Chromium command line flags by passing a list to the `chromeFlags` attribute on the `options` dictionary and then passing this to `eel.start()`

```
web_app_options = {
	'mode': "chrome-app", #or "chrome"
	'port': 8080,
	'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
}

eel.start('main.html', options=web_app_options)
```

#### Exposing functions

In addition to the files in the frontend folder, a Javascript library will be served at `/eel.js`. You should include this in any pages:

```html
<script type="text/javascript" src="/eel.js"></script>
```
Including this library creates an `eel` object which can be used to communicate with the Python side.

Any functions in the Python code which are decorated with `@eel.expose` like this...
```python
@eel.expose
def my_python_function(a, b):
    print(a, b, a + b)
```
...will appear as methods on the `eel` object on the Javascript side, like this...
```javascript
console.log('Calling Python...');
eel.my_python_function(1, 2);   // This calls the Python function that was decorated
```

Similarly, any Javascript functions which are exposed like this...
```javascript
eel.expose(my_javascript_function);
function my_javascript_function(a, b, c, d) {
  if(a < b){
    console.log(c * d);
  }
}
```
can be called from the Python side like this...
```python
print('Calling Javascript...')
eel.my_javascript_function(1, 2, 3, 4)  # This calls the Javascript function
```
When passing complex objects as arguments, bear in mind that internally they are converted to JSON and sent down a websocket (a process that potentially loses information).

#### Eello, World!

Putting this together into a **Hello, World!** example, we have a short HTML page, `web/hello.html`:
```html
<!DOCTYPE html>
<html>
    <head>
        <title>Hello, World!</title>
        
        <!-- Include eel.js - note this file doesn't exist in the 'web' directory -->
        <script type="text/javascript" src="/eel.js"></script>
        <script type="text/javascript">
        
        eel.expose(say_hello_js);               // Expose this function to Python
        function say_hello_js(x) {
            console.log("Hello from " + x);
        }
        
        say_hello_js("Javascript World!");
        eel.say_hello_py("Javascript World!");  // Call a Python function
        
        </script>
    </head>
    
    <body>
        Hello, World!
    </body>
</html>
```

and a short Python script `hello.py`:
```python
import eel

eel.init('web')                     # Give folder containing web files

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('hello.html')             # Start (this blocks and enters loop)
```

If we run the Python script (`python hello.py`), then a browser window will open displaying `hello.html`, and we will see...
```
Hello from Python World!
Hello from Javascript World!
```
...in the terminal, and...
```
Hello from Javascript World!
Hello from Python World!
```
...in the browser console (press F12 to open). 

You will notice that in the Python code, the Javascript function is called before the browser window is even started - any early calls like this are queued up and then sent once the websocket has been established.

#### Return values

While we want to think of our code as comprising a single application, the Python interpreter and the browser window run in separate processes. This can make communicating back and forth between them a bit of a mess, especially if we always had to explicitly *send* values from one side to the other.

Eel supports two ways of retrieving *return values* from the other side of the app, which helps keep the code concise.

##### Callbacks

When you call an exposed function, you can immediately pass a callback function afterwards. This callback will automatically be called asynchrounously with the return value when the function has finished executing on the other side.

For example, if we have the following function defined and exposed in Javascript:
```javascript
eel.expose(js_random);
function js_random() {
  return Math.random();
}
```
Then in Python we can retrieve random values from the Javascript side like so:
```python
def print_num(n):
    print('Got this from Javascript:', n)

# Call Javascript function, and pass explicit callback function    
eel.js_random()(print_num)

# Do the same with an inline lambda as callback
eel.js_random()(lambda n: print('Got this from Javascript:', n))
```
(It works exactly the same the other way around).

##### Synchronous returns

In most situations, the calls to the other side are to quickly retrieve some piece of data, such as the state of a widget or contents of an input field. In these cases it is more convenient to just synchronously wait a few milliseconds then continue with your code, rather than breaking the whole thing up into callbacks.

To synchronously retrieve the return value, simply pass nothing to the second set of brackets. So in Python we would write:
```python
n = eel.js_random()()  # This immeadiately returns the value
print('Got this from Javascript:', n)
```
You can only perform synchronous returns after the browser window has started (after calling `eel.start()`), otherwise obviously the call with hang.

In Javascript, the language doesn't allow us to block while we wait for a callback, except by using `await` from inside an `async` function. So the equivalent code from the Javascript side would be:
```javascript
async function run() {
  // Inside a function marked 'async' we can use the 'await' keyword.
  
  let n = await eel.py_random()();    // Must prefix call with 'await', otherwise it's the same syntax
  console.log('Got this from Python: ' + n);
}

run();
```

### Asynchronous Python

Eel is built on Bottle and Gevent, which provide an asynchronous event loop similar to Javascript. A lot of Python's standard library implicitly assumes there is a single execution thread - to deal with this, Gevent "monkey patches" many of the standard modules such as `time`. This monkey patching is done automatically when you call `import eel`. For convenience, the two most commonly needed methods, `sleep()` and `spawn()` are provided directly from Eel (to save importing `time` and/or `gevent` as well).

In this example...
```python
import eel
eel.init('web')

def my_other_thread():
    while True:
        print("I'm a thread")
        eel.sleep(1.0)
    
eel.spawn(my_other_thread)

eel.start('main.html', block=False)     # Don't block on this call

while True:
    print("I'm a main loop")
    eel.sleep(1.0)
```
...we would then have three "threads" (greenlets) running;
1. Eel's internal thread for serving the web folder
2. The `my_other_thread` method, repeatedly printing **"I'm a thread"**
3. The main Python thread, which would be stuck in the final `while` loop, repeatedly printing **"I'm a main loop"**

### Building a distributable binary

If you want to package your app into a program that can be run on a computer without a Python interpreter installed, you should use **pyinstaller**.

1. Install pyinstaller `pip install pyinstaller`
2. In your app's folder, run `python -m eel [your_main_script] [your_web_folder]` (for example, you might run `python -m eel hello.py web`)
3. This will create a new folder `dist/`
4. Check the contents of this folder for extra modules that pyinstaller is incorrectly including
5. Exclude these using the flag `--exclude module_name`. For example, you might run `python -m eel file_access.py web --exclude win32com --exclude numpy --exclude cryptography`
7. When you are happy that your app is working correctly, add `--onefile --noconsole` flags to build a single executable file

Consult the [documentation for pyinstaller](http://pyinstaller.readthedocs.io/en/stable/) for more options.
