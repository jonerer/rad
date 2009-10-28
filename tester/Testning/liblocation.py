# Python wrapper to the Maemo 4.0 "Chinook" liblocation.  
# Wrapper version 0.1.
#
# Copyright 2008 by Robert W. Brewer < rwb123 at gmail dot com >
# Licensed under GNU LGPL v3.
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# Please see <http://www.gnu.org/licenses/> for a copy of the
# GNU Lesser General Public License.



########################################
# For a documentation overview of liblocation please see:
# http://maemo.org/development/documentation/how-tos/4-x/maemo_connectivity_guide.html#Location
#########################################


import gobject
import ctypes as C
from types import MethodType


########################################
# constants
########################################


(STATUS_NO_FIX, 
 STATUS_FIX,    
 STATUS_DGPS_FIX) = range(3)

(MODE_NOT_SEEN,
 MODE_NO_FIX,
 MODE_2D,
 MODE_3D) = range(4)

NONE_SET     = 0
ALTITUDE_SET = 1<<0
SPEED_SET    = 1<<1
TRACK_SET    = 1<<2
CLIMB_SET    = 1<<3
LATLONG_SET  = 1<<4
TIME_SET     = 1<<5



########################################
# ctypes structure definitions
########################################


class GTypeInstance(C.Structure):
    _fields_ = [('g_class', C.c_ulong)]


class GObject(C.Structure):
    _fields_ = [('g_type_instance', GTypeInstance),
                ('ref_count', C.c_uint),
                ('qdata', C.c_void_p)]


class GPtrArray(C.Structure):
    _fields_ = [('pdata', C.c_void_p),
                ('len', C.c_uint)]


class LocationGPSDeviceSatellite(C.Structure):
    _fields_ = [('prn', C.c_int),
                ('elevation', C.c_int),
                ('azimuth', C.c_int),
                ('signal_strength', C.c_int),
                ('in_use', C.c_int)]


class LocationGPSDeviceFix(C.Structure):
    _fields_ = [('mode', C.c_int),
                ('fields', C.c_uint),
                ('time', C.c_double),
                ('ept', C.c_double),
                ('latitude', C.c_double),
                ('longitude', C.c_double),
                ('eph', C.c_double),
                ('altitude', C.c_double),
                ('epv', C.c_double),
                ('track', C.c_double),
                ('epd', C.c_double),
                ('speed', C.c_double),
                ('eps', C.c_double),
                ('climb', C.c_double),
                ('epc', C.c_double),
                # private, not used yet
                ('pitch', C.c_double),
                ('roll', C.c_double),
                ('dip', C.c_double)]


class CLocationGPSDevice(C.Structure):
    _fields_ = [('parent', GObject),
                ('online', C.c_int),
                ('status', C.c_int),
                ('Cfix', C.POINTER(LocationGPSDeviceFix)),
                ('satellites_in_view', C.c_int),
                ('satellites_in_use', C.c_int),
                ('Csatellites', C.POINTER(GPtrArray))]  # of LocationGPSDeviceSatellite

    def sv_iter(self):
        if not self.Csatellites:
            return
            
        gar = self.Csatellites.contents
        sv_ptr_ptr = C.cast(gar.pdata, 
                            C.POINTER(C.POINTER(LocationGPSDeviceSatellite)))
    
        for i in range(gar.len):
            yield sv_ptr_ptr[i].contents


    def __getattr__(self, name):
        try:
            return C.Structure.__getattr__(self)
        except AttributeError:
            if name == 'fix':
                if self.Cfix:
                    return self.Cfix.contents
                else:
                    return None
            if name == 'satellites':
                return self.sv_iter()
            raise AttributeError




class CLocationGPSDControl(C.Structure):
    _fields_ = [('parent', GObject),
                ('can_control', C.c_int)]


################################################
# gobject C->Python boilerplate from pygtk FAQ
################################################

# this boilerplate can convert a memory address
# into a proper python gobject.
class _PyGObject_Functions(C.Structure):
    _fields_ = [
        ('register_class',
         C.PYFUNCTYPE(C.c_void_p, C.c_char_p,
                           C.c_int, C.py_object,
                           C.py_object)),
        ('register_wrapper',
         C.PYFUNCTYPE(C.c_void_p, C.py_object)),
        ('register_sinkfunc',
         C.PYFUNCTYPE(C.py_object, C.c_void_p)),
        ('lookupclass',
         C.PYFUNCTYPE(C.py_object, C.c_int)),
        ('newgobj',
         C.PYFUNCTYPE(C.py_object, C.c_void_p)),
        ]
    
class PyGObjectCPAI(object):
    def __init__(self):
        addr = C.pythonapi.PyCObject_AsVoidPtr(
            C.py_object(gobject._PyGObject_API))
        self._api = _PyGObject_Functions.from_address(addr)

    def pygobject_new(self, addr):
        return self._api.newgobj(addr)


# call like this:
# Cgobject = PyGObjectCPAI()
# Cgobject.pygobject_new(memory_address)

# to get memory address from a gobject:
#  address = hash(obj)






###################################
# pythonized functions
###################################



def gps_device_get_type():
    return loc_gps_type()


def gps_device_get_new():

    def struct(self):
        ptr = C.cast(C.c_void_p(hash(self)), 
                     C.POINTER(CLocationGPSDevice))
        return ptr.contents

    # create C gobject for gps device
    cgps_dev = gobj_new(gps_device_get_type(), None)

    # wrap in python gobject
    pyobj = Cgobject.pygobject_new(cgps_dev)

    # add a struct() method to hide the ctypes stuff.
    setattr(pyobj, 'struct', MethodType(struct, pyobj, pyobj.__class__))
    return pyobj


def gps_device_reset_last_known(gpsdevice):
    libloc.location_gps_device_reset_last_known(C.c_void_p(hash(gpsdevice)))
    
def gps_device_start(gpsdevice):
    libloc.location_gps_device_start(C.c_void_p(hash(gpsdevice)))

def gps_device_stop(gpsdevice):
    libloc.location_gps_device_stop(C.c_void_p(hash(gpsdevice)))


def gpsd_control_get_default():    
    def struct(self):
        ptr = C.cast(C.c_void_p(hash(self)), 
                     C.POINTER(CLocationGPSDControl))
        return ptr.contents
        

    gpsd_control_ptr = loc_gpsd_control()

    # wrap in python object
    pyobj = Cgobject.pygobject_new(gpsd_control_ptr)

    # add a struct() method to hide the ctypes stuff.
    setattr(pyobj, 'struct', MethodType(struct, pyobj, pyobj.__class__))
    return pyobj

def gpsd_control_start(gpsdcontrol):
    libloc.location_gpsd_control_start(C.c_void_p(hash(gpsdcontrol)))


def gpsd_control_stop(gpsdcontrol):
    libloc.location_gpsd_control_stop(C.c_void_p(hash(gpsdcontrol)))

def gpsd_control_request_status(gpsdcontrol):
    libloc.location_gpsd_control_request_status(C.c_void_p(hash(gpsdcontrol)))



########################################
# initialize library
########################################

# load C libraries
libloc = C.CDLL('liblocation.so.0')
libgobject = C.CDLL('libgobject-2.0.so.0')
Cgobject = PyGObjectCPAI()


# inform ctypes of necessary function prototype information

loc_gps_type = libloc.location_gps_device_get_type
loc_gps_type.restype = C.c_ulong

gobj_new = libgobject.g_object_new
gobj_new.restype = C.c_void_p

loc_gpsd_control = libloc.location_gpsd_control_get_default
loc_gpsd_control.restype = C.POINTER(CLocationGPSDControl)


libloc.location_distance_between.argtypes = [C.c_double, 
                                             C.c_double,
                                             C.c_double,
                                             C.c_double]
libloc.location_distance_between.restype = C.c_double
