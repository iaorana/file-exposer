# swap-exposer.py

![](resized-8187.jpg?raw=true)

This tool is currently under development. At this point it is in the proof of concept stage. The goal of this tool is to aid in the discovery of vim, emacs, and nano swap/temp files that are left on public facing websites. 

# Backstory

This idea was a hybrid of two different tools and ideas that I wanted to try out. The first tool that inspired me was orphan-hunter. It uniquely uses the wayback machine archive to discover orphan files. The second tool I borrowed an idea from is CMSploit. This tool searches for a fixed set of known configuration files related to CMS websites. 

# What does it do?

This tool will do a search query to the wayback machine (www.archive.org) for a requested domain. The response will include every URL that their robots have indexed. This tool then takes the response and filters out pages that are not php, asp, cfm, or cfml. These remaining pages are stored in a set to remove duplicates. It will then do HEAD requests for swap/temp file names based on the scraped URL set. Some sites will respond with HTTP 200 for any given file, which is a problem I had to address. When the program detects a valid swap file it will make a second HEAD request for a incorrect file name to evaluate if it also gets a HTTP 200 code. HEAD was chosen over GET as to not tax the website as much when you're making many requests. 

# Sample output

```
user@user:~/swap-exposer$ python swap-exposer.py website.com
Search query requested for website.com.
Search response received.
Parsing HTML.
Parsing links.
http://website.com/vb/search.php
http://website.com:80/vb/register.php
http://www.website.com:80/vb/showthread.php
http://website.com/b2.php
http://www.website.com:80/vb/calendar.php
http://website.com/vb/calendar.php
http://www.website.com/red/gauntlet/disclaimer.php
http://www.website.com:80/vb/archive/index.php
http://www.website.com/vb/showgroups.php
http://website.com/~cut/config.php~

---- snip ----

145 unique files found.
HEAD requests.
http://website.com/~cut/config.php~.swp found.
http://www.website.com/vb/archive/index.php/f-2.html.swp catchall detected.
http://www.website.com/vb/archive/index.php/f-9.html.swp catchall detected.
http://www.website.com/~twenty/gallery/rss.php.swp found.
http://www.website.com:80/vb/archive/index.php/f-4.html.swp catchall detected.
http://website.com/~cut/config.php.swp found.
```

# Future plans / extending

While this tool's main purpose was to locate swap/temp files for URLs, it might also make sense to add a feature to look for known interesting files. example: .gitignore, .bash_history, .bash_profile, etc..

- ASCII colors, because.

- JSON output option.

- Rate limiting option, this might be useful when scanning large sets of URLs.

- Adding HTTP redirect detection will lower false positives.

- Adding support for a connection timeout configuration option. This would be good for slow servers. 

- I could also see benefit in using search engine responses to find more files that the wayback machine isn't aware of. ex: site: domain.com.
