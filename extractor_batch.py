import mwxml
import mwparserfromhell
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType
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
    CREATE INDEX IF NOT EXISTS ON page_links (links);
""")

session.execute("""
    CREATE TABLE redirects (
        original text PRIMARY KEY,
        redirect text
    );
""")

insert_page_query = "INSERT INTO page_links (title, links, is_redirect) VALUES (?, ?, ?)"
insert_redirect_query = "INSERT INTO redirects (original, redirect) VALUES (?, ?)"
insert_page_stmt = session.prepare(insert_page_query)
insert_redirect_stmt = session.prepare(insert_redirect_query)

# Load wiki dump
file = "enwiki-latest-pages-articles-multistream.xml"
dump = mwxml.Dump.from_file(open(file, "rb"))

page_count = 6_990_400 # Approximate number of wikipedia 'pages' in the dump
pbar = tqdm(total=page_count)
i = 0

MAX_BATCH = 20 * 1024  # ~40KB
batch = BatchStatement(batch_type=BatchType.UNLOGGED)
current_size = 0

def size_of(value):
    return sum(len(str(v)) for v in value)

for page in dump:

    for revision in page:

        title = page.title

        if page.redirect:
            values1 = (title, set(), True)
            values2 = (title, page.redirect)

            row_size = size_of(values1) + size_of(values2)

            if current_size + row_size > MAX_BATCH:
                session.execute(batch)
                batch = BatchStatement(batch_type=BatchType.UNLOGGED)
                current_size = 0

            batch.add(insert_page_stmt, values1)
            batch.add(insert_redirect_stmt, values2)
            current_size += row_size

            pbar.update(1)

            break

        wikicode = mwparserfromhell.parse(revision.text)
        links = set(
            str(link.title).strip()
            for link in wikicode.filter_wikilinks()
            if link.title and not link.title.startswith((
                'File:', 'Image:', 'Special:', 
                'Category:', 'Help:', 'Portal:', 
                'Template:', 'Wikipedia:', 'wikt:'))
        )

        values = (title, links, False)
        row_size = size_of(values)

        if current_size + row_size > MAX_BATCH:
            session.execute(batch)
            batch = BatchStatement(batch_type=BatchType.UNLOGGED)
            current_size = 0

        batch.add(insert_page_stmt, values)
        current_size += row_size

        pbar.update(1)

        break  # only use first revision

# Final execute
if len(batch) > 0:
    session.execute(batch)