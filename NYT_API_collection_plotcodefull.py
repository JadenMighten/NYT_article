#read readmeb4runningapicode.txt before inspecting this code
#import libraries
import requests
import calendar
import time
import nums_from_string
import matplotlib.pyplot as plt
#create lists
wordcountt=[]
firstdate=[]
lastdate=[]
firstdatelnk=[]
lastdatelnk=[]
lnk=[]
pages=[]
remainder=[]
averagewc=[]
numarticles=[]
#generating first date in each month
for year in range (2018,2021):
    year = str(year)
    intyear = int(year)
    month = "01"
    intmonth = int(month)
    day = "01"
    while intmonth<13:
        date=(year +"-"+month+"-"+day)
        datelnk=(year+month+day)
        datelnks=str(datelnk)
        datelnkst=datelnks.strip(" ")
        dates = str(date)
        datest = date.strip(" ")
        intmonth = intmonth+1
        month = ("%02d" % (intmonth,))
        firstdate.append(datest)
        firstdatelnk.append(datelnkst)

#get the dates in my period
firstdates=firstdate[5:25]
firstdateslnk=firstdatelnk[5:25]

#find last date
for f in range (0,20):
    sk=firstdates[f]
    ymd=sk.split("-")
    y=int(ymd[0])
    m=int(ymd[1])
    mo = ("%02d" % (m,))
    last = (calendar.monthrange(y,m))[1]
    final_date = (str(y)+"-"+mo+"-" +str(last))
    final_datelnk = (str(y)+mo+str(last))
    lastdate.append(final_date)
    lastdatelnk.append(final_datelnk)

#get urls of each month
#first date is may 31st
lnk.append("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=Trump&sort=oldest&begin_date=20200531&size=100&api-key=cs5Q9NELoymNh3ENo24GSetljzZGH8jr")
for g in range (0,20):
    apiurldate = ("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=Trump&sort=oldest&begin_date="+firstdateslnk[g]+"&end_date="+lastdatelnk[g]+"&size=100&api-key=cs5Q9NELoymNh3ENo24GSetljzZGH8jr")
    lnk.append(apiurldate)
lnk.append("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=Trump&sort=oldest&begin_date=20200201&end_date=20200227&size=100&api-key=cs5Q9NELoymNh3ENo24GSetljzZGH8jr")

#getnumberofpages
for h in range (0,22):
    url=lnk[h]
    reponse = requests.get(url)
    response = reponse.json()
    numhits = response['response']['meta']['hits']
    intnumhits = int(numhits)
    numpage = (divmod(intnumhits, 10))[0]
    numresult = (divmod(intnumhits, 10))[1]
    remainder.append(numresult)
    pages.append(numpage)
    numarticles.append(intnumhits)
    time.sleep(6)

#create list of months/timeframes
monthxaxis=[]
monthxaxis.append("05/18")

for y in range (0,20):
    xaxis=(firstdates[y][5:7]+"/"+firstdates[y][2:4])
    monthxaxis.append(xaxis)
monthxaxis.append("02/20")
        

#defining function to find number of articles and word count for each article on a single page
def while_loop2():
    wordcounti=0
    j=0
    while j<10:
        wordcount = response['response']['docs'][j]['word_count']
        wordcountb = int(wordcount)
        wordcounti=wordcountb+wordcounti
        return(wordcounti)
        j=j+1
        
#finding average number of articles in each month in my period
totalwc=[]
for k in range (0,22):
    wordcounti=[]
    j=0
    
#finding wordcount for all pages with ten articles
    for m in range (1,(pages[k]-1)):
        apiurl=str(lnk[k])
        apiurls=(apiurl+"&page="+str(m))
        reponse = requests.get(apiurls)
        response = reponse.json()
        while j<10:
            wordcount = response['response']['docs'][j]['word_count']
            wordcountb = int(wordcount)
            wordcounti.append(wordcountb)
            j=j+1    
        time.sleep(6)
    n=0
    wordcount=0
    strk = str(pages[k])
    rem=int(remainder[k])
    
#finding wordcount for all pages with less than ten articles
    while n < rem:
        apiurls=(apiurl+"&page="+str(m))
        reponse = requests.get(apiurls)
        response = reponse.json()
        wordcount = response['response']['docs'][n]['word_count']
        wordcounti.append(wordcount)
        n=n+1
    tot=sum(wordcounti)
    totstr = str(tot)
    totstrn = nums_from_string.get_nums(totstr)
    totalwc.append(totstr)
    
#Calculating average wordcount
    average = ((int(totalwc[k])))/(((10*(int(pages[k])))+(int(remainder[k]))))
    averagewc.append(average)

#creating graph
rcParams['figure.figsize']= 22,6
plt.plot(monthxaxis, averagewc)
plt.title("Average word count of articles over period 05/31/18 to 27/02/20 containing the word 'Trump'")
plt.xlabel("Month")
plt.ylabel("Word count")

            

