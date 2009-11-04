#!/usr/bin/python2.5
#coding: utf-8

import osso, simplejson
name = None
osso_context = None
osso_rpc = None
has_dbus_registered = False

callbacks = {}

def set_name(new_name):
    global name, osso_c, osso_rpc
    name = new_name
    osso_c = osso.Context(name, "0.0.1", False)
    osso_rpc = osso.Rpc(osso_c)

def receive(interface, method, arguments, user_data):
    try:
        if method not in callbacks:
            return "ERROR: no such callback registered"
        if len(arguments) > 0:
            kwargs = simplejson.loads(arguments[0])
            str_kwargs = {}
            for key in kwargs:
                str_kwargs[str(key)] = kwargs[key]
            val = callbacks[method](**str_kwargs)
        else:
            val = callbacks[method]()
        return simplejson.dumps(val)
    except Exception, e:
        # only return strings
        return str(e)

def send(target_name, method, **kwargs):
    if kwargs == {}:
        rpc_args = tuple()
    else:
        rpc_args = (simplejson.dumps(kwargs),)
    if target_name == name:
        # target is local
        if str(method) not in callbacks:
            return "ERROR: no such callback (local) registered"
        if len(kwargs) > 0:
            val = callbacks[str(method)](**kwargs)
        else:
            val = callbacks[str(method)]()
    else:
        val = osso_rpc.rpc_run("rad.%s" % target_name,
            "/rad/%s" % target_name,
            "rad.%s" % target_name,
            method,
            rpc_args,
            wait_reply=True)
        val = simplejson.loads(val)
    return val

def register(cb_name, callback):
    if name is None:
        raise NameError("No name for this handler set.")
    global callbacks, has_dbus_registered
    if cb_name in callbacks:
        raise NameError("callback name already used.")
    if not has_dbus_registered:
        osso_rpc.set_rpc_callback("rad.%s" % name,
            "/rad/%s" % name,
            "rad.%s" % name,
            receive, osso_c)
        has_dbus_registered = True
    callbacks[cb_name] = callback

