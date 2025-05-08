# WikiLink
There is a popular hypothesis, known as six degrees of separation, holding that any two people are separated by a chain of no more than six acquaintances. [^1]<br>
This concept has been popularised by sites such as [Wikipedia Speedruns](https://www.wikipedia.org/wiki/Wikipedia:Wikipedia_Speedruns) and [6 Degrees of Wikipedia](https://www.sixdegreesofwikipedia.com/)[^2]<br><br>
Recently, when I was playing Wikipedia Speedruns with some of my friends we would use 6 Degrees of Wikipedia to see how quickly we could have made connections (compared to the absurd number of routes we took to connect two pages), but found some issues as not all links between articles seemed valid (potentially due to connections being broken due to page updates, different algorithm for denoting what counts as being 'linked' and even the handling of redirects without making it clear to the end user)<br><br>
So I decided to create my own version, using Cassandra (A high availability, highly performant, fault tolerant NoSQL Database)[^3], and Python, as Python is known for making reading large files much easier and is the language I am most confident in.<br>

## My Solution
There are two parts to my solution:

### Page Parsing and Database Populating

### Searching the Nodes


## Future Plans
I would like to develop this further, with the following changes hoping to improve both the creation of the database and user experience:
- Write a MediaWiki XML parsing library in a faster language (probably C++)
- Add a Frontend to allow the user search easily
- Create a node graph of the routes between pages
- Find ways to speed up finding routes between pages

[^1]: https://en.wikipedia.org/wiki/Six_degrees_of_separation
[^2]: https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia#Other_versions
[^3]: https://en.wikipedia.org/wiki/Apache_Cassandra
