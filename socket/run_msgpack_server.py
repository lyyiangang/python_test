import zerorpc

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

    def test(self, buf):
        print(buf)

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()