# WikiLinks
There is a popular hypothesis, known as six degrees of separation, holding that any two people are separated by a chain of no more than six acquaintances. [^1]<br>
This concept has been popularised by sites such as [Wikipedia Speedruns](https://www.wikipedia.org/wiki/Wikipedia:Wikipedia_Speedruns) and [6 Degrees of Wikipedia](https://www.sixdegreesofwikipedia.com/)[^2]<br><br>
Recently, when I was playing Wikipedia Speedruns with some of my friends we would use 6 Degrees of Wikipedia to see how quickly we could have made connections (compared to the absurd number of routes we took to connect two pages), but found some issues as not all links between articles seemed valid (potentially due to connections being broken due to page updates, different algorithm for denoting what counts as being 'linked' and even the handling of redirects without making it clear to the end user)<br><br>
So I decided to create my own version, using Cassandra (A high availability, highly performant, fault tolerant NoSQL Database)[^3], and Python, as Python is known for making reading large files much easier and is the language I am most confident in.<br>

## My Solution
There are two parts to my solution:

### Page Parsing and Database Populating
The first step in parsing the data and populating my database is to actually set up the database.<br>
I decided to keep things simple, and only have two database tables: 'page_links' and 'redirects'<br>
page_links holds the title as text, a set() of all its links, and is_redirect as a boolean of if the page redirects elsewhere.<br>
redirects holds the 'original' (the page the redirect is coming from), and 'redirect' (the page we are redirecting too)<br>
<br>
The second step in my process is to load the wikidump using the 'mwxml' python library, specifically made for the task of parsing mediawiki datadumps. This allows me to access 'pages' and 'revisions' from within the dump without any extra parsing - meaning I can immediately grab a pages current revision and title.<br>
It also allows me to workout if a page has a redirect, so I can execute the logic for that which involves:
- Grab the pages title
- Grab the title of the page we are redirecting too
- Insert the current title, an empty set, and True (for is_redirect) into the 'page_links' DB table
- Insert the current title and the redirect title into the 'redirects' DB table
- break out of the loop early and move onto the next page
If the page is not a redirect, I next construct a set() of all links on said page, excluding wikipedia special tags like File:, Image:, Wikipedia:, etc; then I insert this data into the 'page_links' DB table.<br>
Finally, I update the progress bar and move on

### Searching the Nodes
I chose 3 algorithms that I have learnt to try and implement for this problem:
- Breadth First Search
- Branch and Bound
- Iterative Deepening Depth First Search

#### Breadth First Search [^4]
The simplest search algorithm to implement, Breadth First Search (BFS) gets a node off the queue, checks to see if it is the goal node otherwise it gets all its children (i.e links) and adds them to the queue - before repeating until a solution is found.<br>
The solution found is not necessarily the shortest, as it solely depends on the order the links are added to the queue (in this case the order the links appear on each page)

#### Branch and Bound [^5]
Branch and Bound allows us to efficiently find a solution by exploring and pruning parts of the solution space.<br>
We first start with the beginning page (start_title) and a cost of 0 assigned to that node with new nodes being added by updating their cost by 1.<br>
A priority queue is then used to always explore the cheapest path first.<br>
We also keep track of the best path found so far (shortest one), updating it if we find a new, shorter path - ignoring nodes whose cost is greater than this 'best path'.<br>
<br>
By following these steps, I can ensure that the path generated is guaranteed to be the shortest possible path - although this doesn't mean the algorithm is the fastest out of these options.

#### Iterative Deepening Depth First Search [^6]
Iterative Deepening Depth First Search (IDDFS) works by combining the benefits of BFS (breadth-first search) and DFS (depth-first search) to generate a guaranteed shortest solution in a shorter period of time than branch and bound.<br>
My code achieves this by setting a starting 'depth', checking all paths up to that depth for a solution. If no solution is found, then I increment depth and repeat the process.<br>
To speed up my algorithm and reduce overhead, while keeping it complete, I chose to use two queues, with one queue storing the last nodes at the value of my 'depth', meaning that on the next iteration (i.e after I have increased my depth) I could pickup from where I left off and continue searching quickly, rather than having to retrace old, explored nodes.

## Future Plans
I would like to develop this further, with the following changes hoping to improve both the creation of the database and user experience:
- Write a MediaWiki XML parsing library in a faster language (probably C++ or Java)
- Add a Frontend to allow the user search easily
- Create a node graph of the routes between pages
- Find ways to speed up finding routes between pages

[^1]: https://en.wikipedia.org/wiki/Six_degrees_of_separation
[^2]: https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia#Other_versions
[^3]: https://en.wikipedia.org/wiki/Apache_Cassandra
[^4]: https://en.wikipedia.org/wiki/Breadth-first_search
[^5]: https://en.wikipedia.org/wiki/Branch_and_bound
[^6]: https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
