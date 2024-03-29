# 7.3 Doubly Linked Lists
'''
in a singly linked list, we cannot efficiently delete an arbitrary node from an iterior position of the list if only
given a reference to that node, because we cannot determine the node that immediately precedes the node to be deleted.

to provide greater symmetry, we define a linked list in which each node keeps an explicit reference to the node before it
and a reference to the node after it. such a structure is known as a doubly linked list. 
'''
'''
Header and Trailer Sentinels:

in order to avoid some special cases when operating near the boundaries of a doubly linked list,
it helps to add special nodes at both ends of the list; a header node at the beginning of the list, and a trailer node
at the end of the list. these 'dummy' nodes are known as sentinels (or guards), and they do not store elements of the
primary sequence. 
'''

# 7.3.1 Basic Implementation of a Doubly Linked List
class _DoublyLinkedBase:
    '''A base class providing a doubly linked list representation'''
    
    class _Node:
        '''Lightweight, nonpublic class for storing a doubly linekd node.'''
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next
    
    def __init__(self):
        '''Create an empty list'''
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self):
        '''Return the number of elements in the list'''
        return self._size
    
    def is_empty(self):
        '''Return True if list is empty'''
        return self._size == 0
    
    def _insert_between(self, e, predecessor, successor):
        '''Add element e between two existing nodes and return new node.'''
        newest = self._Node(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest
    
    def _delete_node(self, node):
        '''Delete nonsentinel node from the list and return its element'''
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None # deprecate, help garbage collection
        return element
    
# 7.3.2 Implementing a Deque with a Doubly Linked List
class LinkedDeque(_DoublyLinkedBase):
    '''Double-Ended queue implementation based on a doubly linked list'''
    
    def first(self):
        '''Return (but do not remove) the element at the front of the deque'''
        if self.is_emtpy():
            raise Exception('queue is empty')
        return self._header._next._element
    
    def last(self):
        '''Return (but do not remove) the element at the tail of the deque'''
        if self.is_empty():
            raise Exception('queue is empty')
        return self._trailer._prev._element
    
    def insert_first(self, e):
        '''Add an element to the front of the deque'''
        self._insert_between(e, self._header, self._header._next)

    def insert_last(self, e):
        '''Add an element to the back of the deque'''
        self._insert_between(e, self._trailer._prev, self._trailer)

    def delete_first(self):
        '''Remove and return the element from the front of the deque.
        
        Raise Empty exception if the deque is empty.
        '''
        if self.is_empty():
            raise Exception('queue is empty')
        return self._delete_node(self._header._next)
    
    def delete_last(self):
        '''Remove and return the element from the back of the deque.
        
        Raise Empty exception if the deque is empty.
        '''
        if self.is_empty():
            raise Exception('queue is empty')
        return self._delete_node(self._trailer._prev)
    