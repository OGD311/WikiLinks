from operator import itemgetter

class searchQueue:
    def __init__(self, is_ordered=False):
        self.items = []
        self.ordered = is_ordered

    def get_length(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0
    
    def clear(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def sort(self):
        # Assume that 2nd entry of tuple is key to sort by
        self.items.sort(key=itemgetter(1))

    def show(self):
        print(self.items)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None
        
    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return None
        

    def replace(self, currentItem, replaceItem):
        if not self.is_empty():
            try:
                index = self.items.index(currentItem)
                self.items.pop(index)
                self.items.insert(index, replaceItem)
            except:
                print("Item not in list")
        else:
            print("No items to replace")