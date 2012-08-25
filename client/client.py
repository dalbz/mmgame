import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

MAX  = 65535
s.connect(("localhost", 43278))
print 'Client socket name is', s.getsockname()
delay = 0.1
while True:
    s.send('message #1')
    print 'Waiting up to', delay, 'seconds for a reply'
    s.settimeout(delay)
    try:
        data = s.recv(MAX)
    except socket.timeout:
        delay *= 2 # wait even longer for the next request
        if delay > 2.0:
            raise RuntimeError('I think the server is down')
    except:
        raise # a real error so we let the user see it
    else: 
        break
        
print 'The server says ', repr(data)