import mwxml
import mwparserfromhell
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from tqdm import tqdm

# Cassandra setup
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS wiki
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};        
""")

session.set_keyspace("wiki")

# Initialise Cassandra tables
session.execute("""
    CREATE TABLE page_links (
        title text PRIMARY KEY,
        links text<set>,
        is_redirect bool
    );   
""")

session.execute("""
    CREATE TABLE redirects (
        original text PRIMARY KEY
        redirect text
    );
""")




# Load wiki dump
file = "" # Replace with path to wikidump.xml
dump = mwxml.Dump.from_file(open(file, "rb"))

page_count = 6_990_400 # Approximate number of wikipedia 'pages' in the dump
pbar = tqdm(total=page_count)
