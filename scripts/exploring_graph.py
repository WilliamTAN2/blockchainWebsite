import inputs_outputs, recent_transaction, tree
from collections import namedtuple
import math

Node_fields = ['txid', 'parent', 'average', 'route_len']
Node = namedtuple('Node', Node_fields)


class Graph(object):
    def __init__(self):
        self.nodes_list = []

    def add_node(self, txid, parent, average, route_len):
        self.nodes_list.append(Node(txid, parent, average, route_len))
        print("LA LISTE EST LA ====> \n")
        print(self.nodes_list)
        print("FIN DE LA LISTE\n")

    def get_best_parent_node(self, parent_txid):
        best_parent = Node(None, None, math.inf, None)
        for node in self.nodes_list:
            if node.txid == parent_txid and node.average < best_parent.average:
                best_parent = node
        return best_parent

    def get_average(self, txid):
        """NOT USED ANYMORE"""
        for node in self.nodes_list:
            if node.txid == txid:
                return node.average

    def get_new_average(self, txid, time, route_len):
        """NOT USED ANYMORE"""
        temp_sum = self.get_average(txid) * (route_len - 1) + time
        new_average = temp_sum / route_len
        return new_average


class GlobalVariable(object):
    def __init__(self):
        self.best_average_time = math.inf
        self.best_node = None
        self.source_timestamp = 0

def explore_graph_forward(g, g_v, txid, route_len, time_limit_in_seconds):
    """Set route_len to 1 at the start"""
    listoftransactions = tree.get_children(txid, str(days_to_seconds(2)))

    if route_len == 1:
        g.add_node(txid, None, 0, 0)
        g_v.source_timestamp = tree.get_timestamp(txid)

    for child_txid in listoftransactions:
        time = tree.get_timestamp(txid) - tree.get_timestamp(child_txid)
        child_average_time = (g_v.source_timestamp - tree.get_timestamp(child_txid)) / route_len
        if route_len >= 3 and child_average_time < g_v.best_average_time:
            g_v.best_average_time = child_average_time
            g_v.best_node = Node(child_txid, txid, child_average_time, route_len)
        if time_limit_in_seconds - time >= 0:
            g.add_node(child_txid, txid, child_average_time, route_len)
            explore_graph_forward(g, g_v, child_txid, route_len + 1, time_limit_in_seconds - time)


def explore_graph(g, g_v, txid, route_len, time_limit_in_seconds):
    """Set route_len to 1 at the start"""
    listofprevioustransactions = recent_transaction.getlistofprevioustransactions(txid)

    if route_len == 1:
        g.add_node(txid, None, 0, 0)
        g_v.source_timestamp = recent_transaction.gettimestampfromtxid(txid)

    for child_txid in listofprevioustransactions:
        time = recent_transaction.gettimestampfromtxid(txid) - recent_transaction.gettimestampfromtxid(child_txid)
        child_average_time = (g_v.source_timestamp - recent_transaction.gettimestampfromtxid(child_txid)) / route_len
        if route_len >= 3 and child_average_time < g_v.best_average_time:
            g_v.best_average_time = child_average_time
            g_v.best_node = Node(child_txid, txid, child_average_time, route_len)
        if time_limit_in_seconds - time >= 0:
            g.add_node(child_txid, txid, child_average_time, route_len)
            explore_graph(g, g_v, child_txid, route_len + 1, time_limit_in_seconds - time)


def days_to_seconds(number_of_days):
    number_of_seconds = number_of_days * 86400
    return number_of_seconds


def build_best_path(g, child_node):
    best_path = [child_node]
    best_parent_txid = child_node.parent
    if best_parent_txid is not None:
        best_path += build_best_path(g, g.get_best_parent_node(best_parent_txid))
    return best_path


def test():
    g = Graph()
    g_v = GlobalVariable()
    explore_graph(g, g_v, 'b5f6e3b217fa7f6d58081b5d2a9a6607eebd889ed2c470191b2a45e0dcb98eb0', 1, days_to_seconds(1))
    print(g_v.best_node.average)
    print(build_best_path(g, g_v.best_node))

def test_forward():
    g = Graph()
    g_v = GlobalVariable()
    explore_graph_forward(g, g_v, 'b5f6e3b217fa7f6d58081b5d2a9a6607eebd889ed2c470191b2a45e0dcb98eb0', 1, days_to_seconds(1))
    print(g_v.best_node.average)
    print(build_best_path(g, g_v.best_node))
