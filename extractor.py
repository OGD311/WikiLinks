import mwxml
import mwparserfromhell
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from tqdm import tqdm
from itertools import islice

# Cassandra setup
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS wiki
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};        
""")

session.set_keyspace("wiki")
session.execute("DROP TABLE IF EXISTS page_links;")
session.execute("DROP TABLE IF EXISTS redirects;")

# Initialise Cassandra tables
session.execute("""
    CREATE TABLE page_links (
        title text PRIMARY KEY,
        links set<text>,
        is_redirect boolean
    );   
""")

session.execute("""
    CREATE TABLE redirects (
        original text PRIMARY KEY,
        redirect text
    );
""")

insert_page_query = "INSERT INTO page_links (title, links, is_redirect) VALUES (%s, %s, %s)"

insert_redirect_query = "INSERT INTO redirects (original, redirect) VALUES (%s, %s)"


# Load wiki dump
file = "enwiki-latest-pages-articles-multistream.xml"
dump = mwxml.Dump.from_file(open(file, "rb"))

page_count = 6_990_400 # Approximate number of wikipedia 'pages' in the dump
pbar = tqdm(total=page_count)
i = 0
for page in dump:
   

    for revision in page:

        title = page.title

        if page.redirect:
            session.execute(insert_page_query, (title, set(), True))
            session.execute(insert_redirect_query, (title, page.redirect))
            break

        wikicode = mwparserfromhell.parse(revision.text)
        links = set(
                str(link.title).strip()
                for link in wikicode.filter_wikilinks()
                if link.title and not link.title.startswith((
                    'File:', 'Image:', 'Special:', 
                    'Category:', 'Help:', 'Portal:', 
                    'Template:', 'Wikipedia:'))
                )
        
        session.execute(insert_page_query, (title, links, False))

        break # Only want the first revision

    pbar.update(1)
