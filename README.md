# Pure Todo

A todo list with pure python? What?

## Motivation

Well, this is no way a project to go to production in any case, is just for show and tell! :D I'm advancing in my carrier and learning how WSGI protocol works and how python deals with it is essential to understand how frameworks work and deals with various issues! Once again, I don't want to build a new generation of [FastAPI](https://fastapi.tiangolo.com/) or [Flask](https://flask.palletsprojects.com/en/2.3.x/), I just want to learn how things work under the hood and have some fun in the process, I might learn some advanced stuff that will help me maintain those great frameworks instead of competing with them!

Another nice learning oportunity is on the testing level, doing integration, unit and E2E testing here will leverage my knowledge on the topic too, which is very beneficial!

## How does it work?

Well, python has a protocol standart on conversations between *Web Applciations* and *App Servers* which is called [WSGI](https://pt.wikipedia.org/wiki/Web_Server_Gateway_Interface#:~:text=O%20Web%20Server%20Gateway%20Interface,a%20linguagem%20de%20programa%C3%A7%C3%A3o%20Python.) which stands for *Web Server Gateway Interface*. This was introduced on [PEP 333](https://peps.python.org/pep-0333/) that explains how this communication would work. At the very low level the communication works like this:

    def simple_app(environ, start_response):
        """Simplest possible application object"""
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world!\n']

The entrypoint of the Framework will be a function that will get a `environ` variable with information on the request and a callback function which is the `start_response` that the *App Server* will use to deal with the response that is comming in. The framework have to deal with the headers, status code and response.

There is another better way to implement it, still with pure python, using the `BaseHTTPRequestHandler` which is a wrapper for the function above. We can do more advance stuff like dealing with HTTP verbs and stuff. Really nice!

Well, this is not ideal because you must deal with everything, even the pathing to the static files, but with a simple project like this is easy to have fun doing those low-level stuff.

As *App Server* I'm using the `socketserver` library, also a standart for python! Which deals with port and sockets, I thought on working with it too, but I'm too lazy now. Maybe if I have too much fun here I can think on writing my own *App Server*. But, this guy is also no ideal for production, we have uWSGI and Gunicorn that are way better and heavy-tested.
