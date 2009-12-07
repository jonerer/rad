#!/usr/bin/python2.5
#coding: utf-8

import osso, simplejson, logging
name = None
osso_c = None
osso_rpc = None
has_dbus_registered = False

callbacks = {}

def set_name(new_name):
    global name, osso_c, osso_rpc
    name = new_name
    osso_c = osso.Context(name, "0.0.1", False)
    osso_rpc = osso.Rpc(osso_c)

def receive(interface, method, arguments, user_data):
    global name
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

def send_async(target_name, method, callback=None, **kwargs):
    from types import ListType
    logging.warn("send_async är EXPERIMENTAL, funkar sisådär. använd hellre gobject.timeout_add: http://www.pygtk.org/pygtk2reference/gobject-functions.html")
    def gen_func(cb):
        def func(lol, boll, *args, **kwargs):
            # first two args are teh lol.
            try:
                val = simplejson.loads(args[0])
            except simplejson.JSONDecodeError, e:
                logging.error("fick ett fel i RPC till %s, %s: %s" % (target_name,method,val))
            print "is none? %s" % (cb is None)
            if cb is not None:
                return cb(val)
        return func
    if kwargs == {}:
        rpc_args = tuple()
    else:
        rpc_args = (simplejson.dumps(kwargs),)
    val = osso_rpc.rpc_async_run("rad.%s" % target_name,
        "/rad/%s" % target_name,
        "rad.%s" % target_name,
        method,
        gen_func(callback),
        rpc_args=rpc_args)

def send(target_name, method, args=None, **kwargs):
    if args is not None:
        rpc_args = (simplejson.dumps(args),)
    elif kwargs == {}:
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
        try:
            val = simplejson.loads(val)
        except simplejson.JSONDecodeError, e:
            logging.error("fick ett fel i RPC till %s, %s: %s" % (target_name,method,val))
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

