from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('wiki')

select_node_query = "SELECT * FROM page_links WHERE TITLE = %s;"
select_redirect_query = "SELECT redirect FROM redirects WHERE original = %s;"

class Node:
    def __init__(self, title):
        self.title = title
        self.visited_redirects = set()
        self.load_node(title)

    def load_node(self, title):
        data = session.execute(select_node_query, (title, )).one()
        if data:
            self.title = data.title
            self.links = data.links
            self.is_redirect = data.is_redirect

            if self.is_redirect:
                print(f"Node '{self.title}' is a redirect")
                self.follow_redirect()
        else:
            raise SyntaxError(f"Node with title '{title}' does not exist")

    def follow_redirect(self):
        while self.is_redirect:
            if self.title in self.visited_redirects:
                raise RuntimeError(f"Redirect loop detected at '{self.title}'")
            self.visited_redirects.add(self.title)

            redirect_data = session.execute(select_redirect_query, (self.title, )).one()
            if not redirect_data:
                raise SyntaxError(f"No redirect target found for '{self.title}'")

            new_title = redirect_data.redirect
            print(f"Redirecting to '{new_title}'")
            self.load_node(new_title)

    def get_links(self):
        return self.links

    def node_in_links(self, title):
        return title in self.links

    def __str__(self):
        return f"Node(title='{self.title}', links={len(self.links)}, is_redirect={self.is_redirect})"


if __name__ == "__main__":
    node = Node("Amsterdam")
    print(node)
