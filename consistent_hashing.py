import bisect
import hashlib

class Node(object):
    def __init__(self, node, name):
        self.node = node
        self.name = name

class ConsistentHashRing(object):
    """Implement a consistent hashing ring."""

    def __init__(self, nodes, replicas):
        """Create a new ConsistentHashRing.
        :param replicas: number of replicas.
        """
        self.replicas = replicas
        self.keys = []
        self.nodes = nodes

    def hash(self, key,):
        """Given a string key, return a hash value."""
        key = str(key)
        key = key.encode('utf-8')
        return int(hashlib.md5(key).hexdigest(), 16)

    def get_node(self, key):
        """Return a node, given a key.
        The node replica with a hash value nearest
        but not less than that of the given
        name is returned.   If the hash of the
        given name is greater than the greatest
        hash, returns the lowest hashed node.
        """
        hash_ = self.hash(key)
        start = bisect.bisect(self.keys, hash_)
        if start == len(self.nodes):
            start = 0
        return self.nodes[start]


    def setKeys(self):
        for i in range(len(self.nodes)):
            curKey = self.hash(self.nodes[i].name)
            bisect.insort(self.keys, curKey)