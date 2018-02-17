from .default import view,route,xaal_core

from bottle import request,redirect

import copy

@route('/stats')
@view('stats.mako')
def stats():
    total = 0
    results = {}
    for dev in xaal_core.monitor.devices:
        total = total + 1
        try:
            k = dev.devtype
            results[k]=results[k]+1
        except KeyError:
            results.update({k:1})
    r = {"title" : "Network stats"}
    r.update({"total"   :total})
    r.update({"devtypes":results})
    r.update({"uptime"  : xaal_core.get_uptime()})
    return r


@route('/bottle_info')
@view('bottle_info.mako')
def info():
    r = {"title" : "Bottle Server Info"}
    r.update({"headers" : request.headers})
    r.update({"query"   : request.query})
    r.update({"environ" : copy.copy(request.environ)})
    return r



@route('/devices/<addr>')
@view('device.mako')
def get_device(addr):
    r = {"title" : "device %s" % addr}
    dev = xaal_core.get_device(addr)
    if dev:
        r.update({"dev" : dev})

        if dev.devtype == 'thermometer.basic':
            r.update({"data_is" : "thermometer"})
            r.update({"value"   : dev.attributes['temperature']})

        if dev.devtype == 'hygrometer.basic':
            r.update({"data_is" : "hygrometer"})
            r.update({"value"   : dev.attributes['humidity']})

        if dev.devtype == 'powerrelay.basic':
            r.update({"data_is" : "powerrelay"})
            r.update({"value"   : dev.attributes['power']})
    return r


@route('/devices')
@view('devices.mako')
def get_device():
    r = {"title" : "devices list"}
    devs = xaal_core.monitor.devices
    r.update({"devs" : devs})
    return r




@route('/generic/<addr>')
@view('generic.mako')
def get_device(addr):
    r = {"title" : "device %s" % addr}
    dev = xaal_core.get_device(addr)
    if dev:
        r.update({"dev" : dev})
    return r


@route('/test0')
@view('test0.mako')
def test0():
    r = {"title" : "test0"}
    return r


@route('/test1')
@view('test_home.mako')
def test1():
    r = {"title" : "test1"}
    return r


@route('/test_grid')
@view('grid.mako')
def test_grid():
    return {"title" : "Grid","devices":xaal_core.monitor.devices}


@route('/latency')
def socketio_latency_test():
    redirect('/static/latency.html')


@route('/links')
@view('links.mako')
def links():
    return {'title':'Links'}
