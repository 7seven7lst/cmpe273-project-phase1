import bisect
import hashlib

class Node(object):
    def __init__(self, node, name):
        self.node = node
        self.name = name

class ConsistentHashRing(object):
    def __init__(self, nodes):
        self.keys = []
        self.nodes = nodes

    def hash(self, key):
        key = str(key)
        key = key.encode('utf-8')
        return int(hashlib.md5(key).hexdigest(), 16)

    def get_node(self, key):
        hashed_key = self.hash(key)
        start = bisect.bisect(self.keys, hashed_key)
        if start == len(self.nodes):
            start = 0
        return self.nodes[start]


    def set_keys(self):
        for i in range(len(self.nodes)):
            current_key = self.hash(self.nodes[i].name)
            bisect.insort(self.keys, current_key)