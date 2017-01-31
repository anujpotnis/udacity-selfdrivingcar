
# coding: utf-8

# ## Miniflow

# ### jupyter notebook --script

# In[1]:

class Node(object):
    def __init__(self, inbound_nodes=[]):
        # nodes from which this node receives values
        self.inbound_nodes = inbound_nodes
        # nodes to which this node passes values
        self.outbound_nodes = []
        
        # for each inbound node here, add this node as outbound node to _that_
        ## for inbound we need a distinction between inbound_nodes and self.inbound_nodes since we
        ## passing it in addition to creating it as an instance variable
        for n in self.inbound_nodes:
            n.outbound_nodes.append(self)
        # a calculated value
        self.value = None
        
    def forward(self):
        '''
        Forward propagation
        '''
        raise NotImplemented
        '''
        https://www.quantifiedcode.com/knowledge-base/
        correctness/%60NotImplemented%60%20raised,%20instead%20of%20%60NotImplementedError%60/28OZRVf7
        '''


# In[2]:

class Input(Node):
    def __init__(self):
        # Input node has no inbound nodes, so nothing is passed to node instantiator
        Node.__init__(self)
        
    #Note: Input node is the only node where value may be passed as argument to forward()
    #
    # all other nodes get values of previous nodes from self.inbound_nodes
    #
    # Example:
    # val0 = self.inbound_nodes[0].value
    def forward(self, value=None):
        # overwrite the value if one is passed in
        if value is not None:
            self.value = value


# ## Quiz code

# In[4]:

class Add(Node):
    def __init__(self,x,y):
        # You could access `x` and `y` in forward with
        # self.inbound_nodes[0] (`x`) and self.inbound_nodes[1] (`y`)
        Node.__init__(self,[x,y])
        
    def forward(self):
        """
        Set the value of this node (`self.value`) to the sum of it's inbound_nodes.

        Your code here!
        """
        self.value = self.inbound_nodes[0].value + self.inbound_nodes[1].value


# In[5]:

"""
No need to change anything below here!
Code as is from Udacity
"""


def topological_sort(feed_dict):
    """
    Sort generic nodes in topological order using Kahn's Algorithm.

    `feed_dict`: A dictionary where the key is a `Input` node and the value is the respective value feed to that node.

    Returns a list of sorted nodes.
    """

    input_nodes = [n for n in feed_dict.keys()]

    G = {}
    nodes = [n for n in input_nodes]
    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in G:
            G[n] = {'in': set(), 'out': set()}
        for m in n.outbound_nodes:
            if m not in G:
                G[m] = {'in': set(), 'out': set()}
            G[n]['out'].add(m)
            G[m]['in'].add(n)
            nodes.append(m)

    L = []
    S = set(input_nodes)
    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Input):
            n.value = feed_dict[n]

        L.append(n)
        for m in n.outbound_nodes:
            G[n]['out'].remove(m)
            G[m]['in'].remove(n)
            # if no other incoming edges add to S
            if len(G[m]['in']) == 0:
                S.add(m)
    return L


# In[6]:

'''
** Code as is from Udacity
'''

def forward_pass(output_node, sorted_nodes):
    """
    Performs a forward pass through a list of sorted nodes.

    Arguments:

        `output_node`: A node in the graph, should be the output node (have no outgoing edges).
        `sorted_nodes`: A topologically sorted list of nodes.

    Returns the output Node's value
    """

    for n in sorted_nodes:
        n.forward()

    return output_node.value


# In[ ]:



