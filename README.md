# Crawler for PGR21
A crawler for [PGR21](http://pgr21.com) to collect well normalized Korean corpus.

## Overview
This repository contains a web crawler for [PGR21](http://pgr21.com/) which has well normalized Korean corpus in many domains, such as news, sub-culture, sience, gossips, technologies and politics.
Moreover, a most important thing is that **this site recommends to use a standard language**. So, it is really good to gether a normalized Korean corpus.
Also, a comment data from 2010 has a additional information about parent comment, which can be used for Dialogue Modeling (or Conversation Modeling).
Currently, this crawler was built to crawl only *Free Board* and *QnA Board* for now, but it is extremely easy to change to collect other boards, too. (Just change source URL, probably.)

## Prerequisites
- Python 2.7 or higher
- BeautifulSoup

## Usage
To collect articles and comments from both Free Board and QnA Board from 1st to 70000-th and 1st to 90000-th:

	$ python pgr_crawler.py 1 70000 1 90000

Again, above command means that let crawler to collect a Free Board articles and comments from 1st post to 70000 post, and a QnA articles and comments from 1st post to 90000 post.
Note that **the crawling will be automatically stopped** when the crawler trys to download more than 30 non-existing articles, and this threshold(=30) is hard-coded in the file.

## Result
From the Free Board, the crwaler collects 56,875 articles and 2,470,966 comments from it, and from the Qna Board, the crawler collects 84,515 questions and 794,519 replys from it.
Also, 884,519 dialogues are collected, too.

## Author
Ki Hyun Kim / pointzz.ki@gmail.com