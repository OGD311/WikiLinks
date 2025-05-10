from operator import itemgetter

class searchQueue:
    def __init__(self):
        self.items = []

    def get_length(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0
    
    def clear(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

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