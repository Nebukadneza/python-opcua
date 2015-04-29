import logging
import uuid


class Buffer(object):

    """
    alternative to io.BytesIO making debug easier
    and added a few conveniance methods
    """

    def __init__(self, data):
        self.logger = logging.getLogger(__name__)
        self.data = data

    def __str__(self):
        return "Buffer(size:{}, data:{})".format(len(self.data), self.data)
    __repr__ = __str__

    def __len__(self):
        return len(self.data)

    def read(self, size):
        """
        read and pop number of bytes for buffer
        """
        if size > len(self.data):
            raise Exception("No enough data left in buffer, request for {}, we have {}".format(size, self))
        #self.logger.debug("Request for %s bytes, from %s", size, self)
        data = self.data[:size]
        self.data = self.data[size:]
        #self.logger.debug("Returning: %s ", data)
        return data

    def copy(self, size=None):
        """
        return a copy, optionnaly only copy 'size' bytes
        """
        if size is None:
            return Buffer(self.data)
        else:
            return Buffer(self.data[:size])

    def test_read(self, size):
        """
        read 'size' bytes from buffer, without removing them from buffer
        """
        if size > len(self.data):
            raise Exception("No enough data left in buffer, request for {}, we have {}".format(size, self))
        return self.data[:size]

class SocketClosedException(Exception):
    pass

class SocketWrapper(object):
    """
    wrapper to make it possible to have same api for 
    normal sockets, socket from asyncio, StringIO, etc....
    """
    def __init__(self, sock):
        self.socket = sock

    def read(self, size):
        """
        Receive up to size bytes from socket
        """
        data = b''
        while size > 0:
            chunk = self.socket.recv(size)
            if not chunk:
                raise SocketClosedException("Server socket has closed")
            data += chunk
            size -= len(chunk)
        return data

    def write(self, data):
        self.socket.sendall(data)



def create_nonce():
    return uuid.uuid4().bytes + uuid.uuid4().bytes  # seems we need at least 32 bytes not 16 as python gives us...
