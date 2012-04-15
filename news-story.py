import urllib   #needed to GET the nytimes webpage
import json     #needed to convert string to dictionary
import random   #needed to generate random numbers

#get_from_web is a procedure used in the search engine
#we built in our class.  Here it is used to retrieve
#data from the New York Times API.

def get_from_web(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return None

#load_dictionary is a procedure I built to convert
#a string in JSON format to a python dictionary. After
#cs101 it was amazing how easy it was to search online
#and see from forums and examples and templates how to do
#certain things. Sometimes get_from_web request would not
#return anything so the while loop is used to keep
#trying until it works.

def load_dictionary(url):
    s = None
    while not s:
        s = get_from_web(url)
    return json.loads(s)

#get_recent_headline returns the article title and url
#for one of the 10 most recent updates to the New York
#Times websites using the Times Newswire API. To get
#the code to work, replace "myapikey" with a key obtained
#from developer.nytimes.com

def get_recent_headline():
    url = 'http://api.nytimes.com/svc/news/v3/content/all/all?limit=10&api-key=myapikey'
    d = load_dictionary(url)
    select_article = random.randrange(0,10) #used to randomly select one of the ten article returned
    article_title = d['results'][select_article]['title']
    article_url = d['results'][select_article]['url']
    return article_title, article_url

#get_search_headline returns the article title and url
#for one of the first articles returned from a title
#keyword search of the New York Times Search API.  To get
#the code to work, replace "myapikey" with a key obtained
#from developer.nytimes.com

def get_search_headline(keyword):
    url_start = 'http://api.nytimes.com/svc/search/v1/article?query=title:'
    url_end = '&api-key=myapikey'
    url = url_start + keyword + url_end #concatenate string to place keyword in correct place
    d = load_dictionary(url)
    if d['total'] > 0: #checks to see whether any articles matched the keyword search
        if d['total'] > 10: #checks to see whether there were more than ten article matches
            articles = 10
        else:
            articles = d['total']
        select_article = random.randrange(0,articles) #selects one of the first 10 (or fewer if not ten total matches)
        article_title = d['results'][select_article]['title']
        article_url = d['results'][select_article]['url']
        return article_title, article_url
    else:
        return None, None

#keyword_from_end returns a keyword from the title, starting
#at the end of the title and working backwards looking for
#words that are at least 4 characters long and that have not
#been used before.

def keyword_from_end(title,used_keywords):
    words = title.split()
    words.reverse() #reverses the order of the string. could have also used .pop() in a loop instead of the for loop used here
    for s in words:
        if s not in used_keywords and len(s) > 3:
            used_keywords.append(s)
            return s
    backup_keywords = ['happiness','peace','joy','good','great','wonderful','incredible','amazing','super','perfect']
    for s in backup_keywords: #if there are no eligible keywords in the title, the list above is used to fill in the gap, kind of a subliminal message
        if s not in used_keywords:
            used_keywords.append(s)
            return s

#get_news_story is the whole point of all this code.  it returns
#a list of 10 elements with each element containing a sublist with
#two elements each, the title of an article and a url for the article.
#The first article is one of the 10 most recent articles from the New
#York Times website, and each subsequent article title contains a keyword
#found in the previous article.  Because the words are repeated, all
#of the article headlines can be read together like a story.  Though the
#articles usually aren't really related, they kind of sound like they
#are and remind us that everything is connected.  API keys have been
#deleted from this code but can be obtained from developer.nytimes.com.
#A live implementation of this code can be found at news-story.appspot.com.

def get_news_story(used_keywords, used_titles, used_urls):
    seed_title, seed_url = get_recent_headline()
    p = [[seed_title,seed_url]] #creates the structure of the news story with the recent article
    i = 1
    while i < 10: #loops to add 9 additional articles
        keyword = keyword_from_end(p[i-1][0],used_keywords) #finds a keyword from the previous article
        next_title, next_url = get_search_headline(keyword)
        if next_title and (next_title not in used_titles) and (next_url not in used_urls): #checks to make sure an article was returned and that the headline and url has not been used before.
            p.append([next_title,next_url])
            used_used_titles.append(next_title)
            used_urls.append(next_url)
            i = i + 1
    return p

#the following initialize the lists that are mutated within the procedures
used_keywords = []
used_titles = []
used_urls = []

#create a news story and assign it to the variable news_story
news_story = get_news_story(used_keywords, used_titles, used_urls)

#print the news story with the URLs to each of the articles
for e in news_story:
    print e[0] ' (' + e[1] + ').'

