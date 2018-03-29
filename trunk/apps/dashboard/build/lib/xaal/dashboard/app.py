from gevent import monkey; monkey.patch_all()


from bottle import default_app,debug,get,redirect,static_file


from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler


from pages import default_pages
from core import xaal_core
from core import sio 

@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static/')

@get('/')
def goto_home():
    redirect('/test_grid')

def foo():
    from bottle import request
    return "Foo [%s]" % request.environ['REMOTE_ADDR']

    
def run():
    """ start the xAAL stack & launch the HTTP stuff"""
    xaal_core.setup()
    # debug disable template cache & enable error reporting
    debug(True)
    bottle_app = default_app()
    app = sio.setup(bottle_app)
    bottle_app.route('/foo1', ['GET', 'POST'], foo)

    
    server = WSGIServer(("", 9090), app, handler_class=WebSocketHandler)
    server.serve_forever()
    
def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye...")
    
if __name__ == '__main__':
    main()
