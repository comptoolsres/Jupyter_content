import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ch 12 Networked Programs

    Chapter 12 of Py4E gets into networked programs, primarily using HyperText Transfer Protocol (http).

    ## Sockets

    This chapter introduces the concept of a **socket**. This is something that will continue to come up, so is important to understand.

    In many ways, a socket is like a file handle--it provides access to the information, not the information itself. However, a socket is different in that it provides **two-way** communication for sending *and* receiving information.

    Here, we'll use sockets to connect to a web server and get the contents of a web page. Different from opening a file on disk, more coordination is needed between your computer and the web server to transmit data, confirm receipt of data, etc. Later, we'll use sockets to connect to databases. And again, coordination and established protocols for sending and receiving data come into play.

    ## Protocols

    As described in the text, for two computers to communicate successfully, they need to be following some protocol, or established procedures for communicating. HTTP is one protocol. We looked briefly at the SFTP (Secure File Transfer Protocol) earlier in the semester for transferring files from our computers to the cluster. Other protocols you may be familiar with include Internet Message Access Protocol (IMAP), Post Office Protocol version 3 (POP3) and Simple Mail Transfer Protocol (SMTP) all used for email systems.

    There are many protocols for different types of communications, the important thing is that you need to establish which protocol is being used and follow the specifications of that protocol.

    ## 12.2 The world’s simplest web browser (p. 146)

    Here's the code for `socket1.py` (remember these are in the code3 directory of the repository).
    """)
    return


@app.cell
def _():
    import socket
    _mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _mysock.connect(('data.pr4e.org', 80))
    cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
    _mysock.send(cmd)
    while True:
        _data = _mysock.recv(512)
        if len(_data) < 1:
            break
        print(_data.decode(), end='')
    # Code: http://www.py4e.com/code3/socket1.py
    _mysock.close()
    return (socket,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that if you navigate to [http://data.pr4e.org/romeo.txt](http://data.pr4e.org/romeo.txt) in your browser, you see the content, but not the headers--your web browser uses the headers to understand the content and format it correctly for you.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12.3 Retrieving an image of HTTP (p. 148)

    Take a look at the `urljpeg.py` script, which downloads an image, and the information on the script in the text.
    """)
    return


@app.cell
def _(socket):
    import time
    HOST = 'data.pr4e.org'
    PORT = 80
    _mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _mysock.connect((HOST, PORT))
    _mysock.sendall(b'GET http://data.pr4e.org/cover3.jpg HTTP/1.0\r\n\r\n')
    count = 0
    picture = b''
    while True:
        _data = _mysock.recv(5120)
        if len(_data) < 1:
            break
        count = count + len(_data)
        print(len(_data), count)
        picture = picture + _data
    _mysock.close()
    pos = picture.find(b'\r\n\r\n')
    print('Header length', pos)
    print(picture[:pos].decode())
    picture = picture[pos + 4:]
    _fhand = open('stuff.jpg', 'wb')
    _fhand.write(picture)
    _fhand.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Hopefully most of this makes some sense, but starts looking kind of messy...The next sections will show you that while you *can* work at this low-level and write code to speak directly to the remote server, there are modules to simplify this. But fundamentally, they provide an easier user experience to the same functionality.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12.4 Retrieving web pages with `urllib`

    The `urllib` module makes getting stuff from the web a bit easier. The `socket1.py` script above can be simplified to:
    """)
    return


@app.cell
def _():
    import urllib.request
    _fhand = _urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
    for line in _fhand:
    # Code: http://www.py4e.com/code3/urllib1.py
        print(line.decode().strip())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice that `urllib` sits between the script and the socket to make an opened socket look just like a file handle and we can treat the web page in much the same way as we treat a local file.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12.5 Reading binary files using `urllib`

    And the rather messy `urljpg.py` to download an image is simplified to:
    """)
    return


@app.cell
def _():
    import urllib.request, urllib.parse, urllib.error
    img = _urllib.request.urlopen('http://data.pr4e.org/cover3.jpg').read()
    _fhand = open('cover3.jpg', 'wb')
    _fhand.write(img)
    _fhand.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The chapter goes on to show how to write out chunks of the file so as not to accumulate everything in RAM.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12.7 Parsing HTML using regular expressions (p. 152)

    We could write our own scripts to parse HTML looking for information. The example here is using a regular expression to search for a link and make a list of links on a page.

    Run `urlregex.py` on some site, google.com for example:

    ```bash
    [magitz@login8 code3]$ python3 urlregex.py
    Enter - http://google.com
    http://www.google.com/imghp?hl=en&tab=wi
    http://maps.google.com/maps?hl=en&tab=wl
    https://play.google.com/?hl=en&tab=w8
    http://www.youtube.com/?gl=US&tab=w1
    http://news.google.com/nwshp?hl=en&tab=wn
    https://mail.google.com/mail/?tab=wm
    https://drive.google.com/?tab=wo
    https://www.google.com/intl/en/options/
    http://www.google.com/history/optout?hl=en
    https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=http://www.google.com/
    https://plus.google.com/116899029375914044550
    [magitz@login8 code3]$
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Unfortunately, not all web pages follow HTML guidelines totally and sometimes pages can be really hard to parse. Tags can be upper and lower case, some closing tags are optional, etc. It can quickly get quite complex.

    ## 12.8 Parsing HTML using BeautifulSoup

    As I mentioned earlier, whatever you are trying to do, look for a module to make your life easier. If you need to parse HTML, don't start trying to write your own script to do it, look at available modules. One is `BeautifulSoup` available from crummy.com--some people sure have fun naming things!
    """)
    return


@app.cell
def _():
    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = input('Enter - ')
    html = _urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    for tag in tags:
        print(tag.get('href', None))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where to go from here?

    There's lots of data on the web and lots of our world lives online..Explore options and think about data sources you are interested in.

    The next chapter goes beyond getting information from web pages to interacting with networked applications using API (Application Programming Interfaces)
    """)
    return


if __name__ == "__main__":
    app.run()
