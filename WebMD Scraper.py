#!/usr/bin/env python
# coding: utf-8

# In[36]:


import random
import requests
import csv
import time
from bs4 import BeautifulSoup
import re
import pandas as pd


# In[69]:


def extractPageInfo(posts,csvname):
        for post in posts:
            #find review info
            reviewerInfo = post.find('p', class_="reviewerInfo").text

            #find reviewer age range
            agePattern = re.compile("\d+-\d+")
            age = agePattern.findall(reviewerInfo)
            if age:
                age = age[0]
            else:
                age = None

            #find duration of use
            durationPattern =  re.compile("on Treatment for (\w+.+) \(Patient\) ")
            duration = durationPattern.findall(reviewerInfo)
            if duration:
                duration = duration[0]
            else:
                duration = None

            #find ratings
            ratingsContainer= post.find('div', id="ctnStars")
            ratePattern = re.compile("\d")
            
            effectiveness = ratingsContainer.find('div', class_="catRatings firstEl clearfix").find('span', class_="current-rating").text
            effectiveness = ratePattern.findall(effectiveness)
            effectiveness = int(effectiveness[0])
            
            easeofuse = ratingsContainer.find('div', class_="catRatings clearfix").find('span', class_="current-rating").text
            easeofuse = ratePattern.findall(easeofuse)
            easeofuse = int(easeofuse[0])
            
            satisfaction = ratingsContainer.find('div', class_="catRatings lastEl clearfix").find('span', class_="current-rating").text
            satisfaction = ratePattern.findall(satisfaction)
            satisfaction = int(satisfaction[0])

            #find comment
            comment = post.find('p', attrs={"class":"comment","style":"display:none",}).text
            commentPattern = re.compile("Comment:(.+)")
            comment= commentPattern.findall(comment)
            if comment:
                comment = comment[0]
            else:
                comment = None


            post_line = [age, duration, effectiveness, easeofuse, satisfaction, comment]
            with open(csvname, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(post_line)


# In[70]:


'''Scrapes all the reviews for a single drug by calculating the number of pages of reviews'''
def singleDrugInfo(link, csvname):
    url = link
    # Headers to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Returns a requests.models.Response object
    page = requests.get(url, headers=headers)

    #create the soup
    soup = BeautifulSoup(page.text, 'html.parser')

    #search the soup for the desired tags
    posts = soup.find_all("div", class_="userPost")

    ## determine number of pages. 
    pages = soup.find("div", class_="postPaging").text
    pagePattern = re.compile("of (\d+)")
    pagenum = pagePattern.findall(pages)
    pagenum = (list(map(int, pagenum))[0])//5

    for x in range(pagenum+1):
        urlPattern = re.compile("&pageIndex=\d+")
        url = urlPattern.sub("&pageIndex="+str(x), url)
        print("working on this url ", url)
        
        # Returns a requests.models.Response object
        page = requests.get(url, headers=headers)
        
        #create the soup
        soup = BeautifulSoup(page.text, 'html.parser')
        
        #search the soup for the desired tags
        posts = soup.find_all("div", class_="userPost")
        
        extractPageInfo(posts, csvname) 
        
        time.sleep(2)
        



    


# In[71]:


'''input: a dictionary of urls where the key is the desired csv name and the value is the url to be used'''
def multipleDrugInfo(urls):
    for url in urls:
        csvname = url
        link = urls[url]
        singleDrugInfo(link, csvname)
        
        


# In[ ]:


## compile dictionary of urls and csvnames from webmd
528106


# In[76]:


data = pd.read_csv("junelfe.csv")
data.head(10)


# In[77]:


data.tail(10)


# ## -------------------------Anything below this line is scratch work -----------------------------

# In[8]:


url = "https://www.webmd.com/drugs/drugreview-77116-Junel-FE-1-20-28-oral.aspx?drugid=77116&drugname=Junel-FE-1-20-28-oral"
# Headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object
page = requests.get(url, headers=headers)

#create the soup
soup = BeautifulSoup(page.text, 'html.parser')

#search the soup for the desired tags
posts = soup.find_all("div", class_="userPost")

## determine number of pages. 
pages = soup.find("div", class_="postPaging").text
pagePattern = re.compile("of (\d+)")
pagenum = pagePattern.findall(pages)
pagenum = list(map(int, pagenum))[0]
pagenum= pagenum//5
print(pagenum)


# In[57]:


## locate necessary elements
for post in posts:
    #find review info
    reviewerInfo = post.find('p', class_="reviewerInfo").text
    
    #find reviewer age range
    agePattern = re.compile("\d+-\d+")
    age = agePattern.findall(reviewerInfo)
    print(age[0])
    
    #find duration of use
    durationPattern =  re.compile("on Treatment for (\w+.+) \(Patient\) ")
    duration = durationPattern.findall(reviewerInfo)
    #print(str(duration[0]))
    
    #find ratings
    ratingsContainer= post.find('div', id="ctnStars")
    ratePattern = re.compile("\d")
    effectiveness = ratingsContainer.find('div', class_="catRatings firstEl clearfix").find('span', class_="current-rating").text
    effectiveness = ratePattern.findall(effectiveness)
    easeofuse = ratingsContainer.find('div', class_="catRatings clearfix").find('span', class_="current-rating").text
    easeofuse = ratePattern.findall(easeofuse)
    satisfaction = ratingsContainer.find('div', class_="catRatings lastEl clearfix").find('span', class_="current-rating").text
    satisfaction = ratePattern.findall(satisfaction)
    print(int(satisfaction[0]))
    
    #find comment
    comment = post.find('p', attrs={"class":"comment","style":"display:none",}).text
    commentPattern = re.compile("Comment:(.+)")
    comment= commentPattern.findall(comment)
    print(comment[0])




## find next page link

next_button = soup.find("div", class_="postPaging")
next_page_link = next_button.find("a").attrs['href']
next_page_link = "https://www.webmd.com"+next_page_link
print(next_page_link)
    


# In[6]:


counter = 1

while (counter <= 5):
    posts = soup.find_all("div", class_="userPost")
    print("going through ", counter, "page")
    print("going through ", counter, "page")
    print("url is ", url)
    
    for post in posts:
        #find review info
        reviewerInfo = post.find('p', class_="reviewerInfo").text

        #find reviewer age range
        agePattern = re.compile("\d+-\d+")
        age = agePattern.findall(reviewerInfo)

        #find duration of use
        durationPattern =  re.compile("on Treatment for (\w+.+) \(Patient\) ")
        duration = durationPattern.findall(reviewerInfo)

        #find ratings
        ratingsContainer= post.find('div', id="ctnStars")
        ratePattern = re.compile("\d")
        effectiveness = ratingsContainer.find('div', class_="catRatings firstEl clearfix").find('span', class_="current-rating").text
        effectiveness = ratePattern.findall(effectiveness)
        easeofuse = ratingsContainer.find('div', class_="catRatings clearfix").find('span', class_="current-rating").text
        easeofuse = ratePattern.findall(easeofuse)
        satisfaction = ratingsContainer.find('div', class_="catRatings lastEl clearfix").find('span', class_="current-rating").text
        satisfaction = ratePattern.findall(satisfaction)

        #find comment
        comment = post.find('p', attrs={"class":"comment","style":"display:none",}).text
        commentPattern = re.compile("Comment:(.+)")
        comment= commentPattern.findall(comment)


        post_line = [age, duration, effectiveness, easeofuse, satisfaction, comment]
        with open('junelfe.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(post_line)

    counter += 1
        
    next_button = soup.find("div", class_="postPaging")
    next_page_link = next_button.find("a").attrs['href']
    next_page_link = "https://www.webmd.com"+next_page_link
    
    wait_time = [5, 10, 15]
    time.sleep(random.choice(wait_time))
    page = requests.get(next_page_link, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    url = next_page_link


# In[1]:


# Install a conda package in the current Jupyter kernel
import sys
get_ipython().system('conda install --yes --prefix {sys.prefix} beautifulsoup4 ')

