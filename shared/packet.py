#coding: utf-8
import simplejson
from datetime import datetime

type_priority = {}
type_priority["login"] = 1.

class Packet(object):
    def __init__(self, type, **data):
        self.type = type # a string
        self.data = data
        self.timestamp = datetime.now()

        if type in type_priority:
            self.priority = type_priority[type]
        else:
            self.priority = 0.5

    @classmethod
    def from_str(cls, data):
        #print data
        #print type(data)
        datadict = simplejson.loads(data)
        a = Packet(datadict["type"])
        a.timestamp = datetime.fromtimestamp(float(datadict["timestamp"]))
        a.data = simplejson.loads(datadict["data"])
        a.priority = datadict["priority"]
        return a

    def __str__(self):
        di = {}
        di["type"] = self.type
        di["data"] = simplejson.dumps(self.data)
        di["timestamp"] = self.timestamp.strftime("%s")
        di["priority"] = self.priority
        return simplejson.dumps(di)

if __name__ == "__main__":
    a = Packet("login", username="lolboll", password="boll_lol")
    print str(a)
    #print a.timestamp
    assert str(a) == str(Packet.from_str(str(a)))
    #print b
    c = Packet("ping") #works with None-data?
    assert str(c) == str(Packet.from_str(str(c)))
    #print Packet.from_net(str(c)).data
    print "shit works!"

