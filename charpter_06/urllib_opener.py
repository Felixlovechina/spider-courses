import urllib2, httplib, socket

# this class ensures user to speicify the network interface which urllib2 uses

class BindableHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        """Connect to the host and port specified in __init__."""
        self.sock = socket.socket()
        self.sock.bind((self.source_ip, 0))
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host,self.port))

def BindableHTTPConnectionFactory(source_ip):
    def _get(host, port=None, strict=None, timeout=0):
        bhc=BindableHTTPConnection(host, port=port, strict=strict, timeout=timeout)
        bhc.source_ip=source_ip
        return bhc
    return _get

class BindableHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(BindableHTTPConnectionFactory('127.0.0.1'), req)

opener = urllib2.build_opener(BindableHTTPHandler)
opener.open("http://google.com/").read() # Will fail, 127.0.0.1 can't reach google.com.