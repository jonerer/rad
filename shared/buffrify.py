#coding: utf-8
import simplejson

def split_buffer(buffer):
    if "\r\n\r\n" in buffer:
        delim_pos = buffer.find("\r\n\r\n")
        con_len = buffer[:delim_pos]
        con_len = int(con_len[con_len.find(" ")+1:])
        rest = buffer[delim_pos+4:]
        if len(rest) >= con_len:
            return rest[:con_len], rest[con_len:]
    return None

def create_pack(data):
    utf = data.encode("utf-8")
    utf = data
    return "Content-Length: %s\r\n\r\n%s" % (len(utf), utf)

if __name__ == "__main__":
    assert split_buffer("Co") is None
    assert split_buffer("Content-Length: 120\r\n\r\nhästar är fula") is None
    assert split_buffer("Content-Length: 10\r\n\r\n0123456789") == ("0123456789", "")
    assert split_buffer("Content-Length: 10\r\n\r\n0123456789Cont") ==  ("0123456789", "Cont")
    assert split_buffer("Content-Length: 4\r\n\r\n1234Content-Length: 4\r\n\r\n5678Content") ==  ("1234", "Content-Length: 4\r\n\r\n5678Content")
    
    assert create_pack("lolboll") == "Content-Length: 7\r\n\r\nlolboll"

    print "ace."
