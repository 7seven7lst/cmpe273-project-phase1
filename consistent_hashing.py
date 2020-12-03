import bisect
import hashlib

class Node(object):
    def __init__(self, node, name):
        self.node = node
        self.name = name

class ConsistentHashRing(object):
    def __init__(self, nodes):
        self.ring = dict() # hashed-key => node
        for node in nodes:
            hashed_key = self.hash(node.name)
            self.ring[hashed_key] = node
        self.ring = dict(sorted(self.ring.items()))

    def hash(self, name):
        key = str(name).encode('utf-8')
        return int(hashlib.md5(key).hexdigest(), 16) % (2**32)

    def add_node(self, node):
        hashed_key = self.hash(node.name)
        self.ring[hashed_key] = node
        self.ring = dict(sorted(self.ring.items()))

    def remove_node(self, node):
        hashed_key = self.hash(node.name)
        self.ring.pop(hashed_key, None)
        self.ring = dict(sorted(self.ring.items()))

    def get_node(self, key):
        # return current node, and next node
        hashed_key = self.hash(key)
        key_list = list(self.ring.keys())
        last_key = int(key_list[-1])
        first_key = int(key_list[0])
        nodes = list(self.ring.values())
        if (hashed_key > last_key):
            return nodes[0]
        elif (hashed_key <= first_key):
            return nodes[0]
        else:
            for k, v in self.ring.items():
                if (hashed_key > k):
                    # starting from smallest key, skip if
                    # hashed key is greater
                    continue
                else:
                    return v