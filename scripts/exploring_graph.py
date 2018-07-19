import inputs_outputs, recent_transaction
from collections import namedtuple

Node_fields = ['txid', 'parent', 'average', 'number_of_nodes']
Node = namedtuple('Node', Node_fields)


class Graph(object):
    def __init__(self):
        self.nodes_list = []

    def add_node(self, txid, parent, average, number_of_nodes):
        self.nodes_list.append(Node(txid, parent, average, number_of_nodes))
        print("LA LISTE EST LA ====> \n")
        print(self.nodes_list)
        print("FIN DE LA LISTE\n")

    def get_average(self, txid):
        for node in self.nodes_list:
            if node.txid == txid:
                return node.average

    def get_new_average(self, txid, time, number_of_nodes):
        temp_sum = self.get_average(txid) * (number_of_nodes - 1) + time
        new_average = temp_sum / number_of_nodes
        return new_average


def exploregraph(g, txid, number_of_nodes, time_limit_in_seconds):
    """Set number_of_nodes to 1 at the start"""
    listofprevioustransactions = recent_transaction.getlistofprevioustransactions(txid)

    if number_of_nodes == 1:
        g.add_node(txid, None, 0, 0)

    for child_txid in listofprevioustransactions:
        time = recent_transaction.gettimestampfromtxid(txid) - recent_transaction.gettimestampfromtxid(child_txid)
        if time_limit_in_seconds - time >= 0:
            g.add_node(child_txid, txid, g.get_new_average(txid, time, number_of_nodes), number_of_nodes)
            exploregraph(g, child_txid, number_of_nodes + 1, time_limit_in_seconds - time)
    return g.nodes_list

def days_to_seconds(number_of_days):
    number_of_seconds = number_of_days * 86400
    return number_of_seconds

def test():
    g = Graph()
    exploregraph(g, 'b5f6e3b217fa7f6d58081b5d2a9a6607eebd889ed2c470191b2a45e0dcb98eb0', 1, days_to_seconds(1))
