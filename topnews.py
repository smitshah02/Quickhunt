# times file
import csv 
import requests 
import xml.etree.ElementTree as ET 
import pandas as pd
from textblob import TextBlob
import pandas as pd
from itertools import islice
import nltk
from nltk.sentiment import SentimentAnalyzer
from nltk.classify.scikitlearn import SklearnClassifier
from newspaper import Article
from flask import Flask, request, render_template
  
def loadRSS(): 
  
    # url of rss feed 
    url = 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms'
  
    # creating HTTP response object from given url 
    resp = requests.get(url) 
  
    # saving the xml file 
    with open('topnewsfeed.xml', 'wb') as f: 
        f.write(resp.content) 
          
  
def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    newsitems = [] 
  
    # iterate news items 
    for item in root.findall('./channel/item'): 
  
        # empty news dictionary 
        news = {} 
  
        # iterate child elements of item 
        for child in item: 
  
            # special checking for namespace object content:media 
            if child.tag == '{http://search.yahoo.com/mrss/}content': 
                news['media'] = child.attrib['url'] 
            else: 
                news[child.tag] = child.text.encode('utf8')
        # append news dictionary to news items list 
        newsitems.append(news) 
      
    # return news items list 
    return newsitems 
  
  
def savetoCSV(newsitems, filename): 
  
    # specifying the fields for csv file 
    fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media'] 
  
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
  
        # creating a csv dict writer object 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
  
        # writing headers (field names) 
        writer.writeheader() 
  
        # writing data rows 
        writer.writerows(newsitems) 
  
      
def main(): 
    # load rss from web to update existing xml file 
    loadRSS() 
  
    # parse xml file 
    newsitems = parseXML('topnewsfeed.xml') 
  
    # store news items in a csv file 
    savetoCSV(newsitems, 'topnews.csv') 
      
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 


#sentimentanalysis on title

df_survey_data = pd.read_csv("topnews.csv")
COLS = ['title','polarity','sentiment']
df = pd.DataFrame(columns=COLS)

for index, row in islice(df_survey_data.iterrows(), 0, None):
    new_entry = []
    text_lower =(row[1])
    blob = TextBlob(text_lower)
    sentiment = blob.sentiment

    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity

    if polarity >= 0.05 : 
        sent = 'Positive'    
        result = ['pos']
  
    elif polarity <= - 0.05 : 
        sent = "Negative" 
        result = ['neg']
  
    else : 
        sent = "Neutral"
        result = ['neu']

    new_entry += [row[1],polarity,sent]

    single_survey_sentimet_df = pd.DataFrame([new_entry], columns=COLS)
    df = pd.concat([df,single_survey_sentimet_df])

df.to_csv("topnewsheadlines.csv", mode='w', columns=COLS, index=False, encoding="utf-8")

# link file

with open("topnewsnews.csv", "r") as csv_file:
   csv_reader = csv.DictReader(csv_file)

   with open("topnewslink.csv","w") as new_file:
    fieldnames=['link']
    csv_writer=csv.DictWriter(new_file,fieldnames=fieldnames,delimiter=',')
    csv_writer.writeheader()
    for line in csv_reader:
        del line['title']
        del line['guid']
        del line['pubDate']
        del line['media']
        del line['description']
        csv_writer.writerow(line)


#scrapping data from links

art = []
with open('topnewslink.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for url in row['link'][1:-1].split(','):
            a=(url.replace("'",""))
            url=(a)
            article=Article(url)
            article.download()
            article.parse()
            article.nlp()
            #at=(article.text)
            suma=(article.summary)
            #img=(article.imgage)
            art.append([suma])
            #art.append([img])
            art.append([])

with open('topnewssummary.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['article_sum'])
    writer.writerows(art)

sn=20

df = pd.read_csv('topnewsheadlines.csv')
titles = list(df.iloc[:, 0].values)
sentiment = list(df.iloc[:, 2].values)

df_link = pd.read_csv('topnewslink.csv')
links = list(df_link.iloc[:, 0].values)

df_sum = pd.read_csv('topnewssummary.csv')
summ = list(df_sum.iloc[:, 0].values)


for i in range(0,len(links)):
  links[i] = links[i][2:]
  links[i] = links[i][:-1]
  #print(links)

for i in range(0,len(titles)):
  titles[i] = titles[i][2:]
  titles[i] = titles[i][:-1]
  #print(titles)


def passon():
  return (sn, summ, titles, sentiment, links)

