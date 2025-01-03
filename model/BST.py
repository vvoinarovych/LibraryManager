class TreeNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        def _insert(node, key, data):
            if not node:
                return TreeNode(key, data)
            if key < node.key:
                node.left = _insert(node.left, key, data)
            else:
                node.right = _insert(node.right, key, data)
            return node
        self.root = _insert(self.root, key, data)

    def search(self, key):
        def _search(node, key):
            if not node or node.key == key:
                return node
            if key < node.key:
                return _search(node.left, key)
            return _search(node.right, key)
        return _search(self.root, key)