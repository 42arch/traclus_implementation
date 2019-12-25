from linked_list import LinkedList, LinkedListNode

list = LinkedList()

node = LinkedListNode(81)

list.add_last(1)
list.add_last(6)
list.add_last(10)
list.add_last(44)
list.add_first(80)
list.add_first(800)
list.add_last_node(node)

for i in list:
    print(i)

# list.remove_node(node)
print('//////////////')
# print(list.get_first())
# print(list.get_last())
for i in list:
    # list.remove_node(i)
    print(i)

print(list.empty())
# print(list[1])
