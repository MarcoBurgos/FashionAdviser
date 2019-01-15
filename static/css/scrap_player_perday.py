import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import lxml.html as lh
import pandas as pd

# Browser
cj = cookielib.LWPCookieJar()
br = mechanize.Browser()

# Cookie Jarcj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

user = "mavi@alphacreativa.com"
pwd = "uDnYzS10"

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('http://origin.milb.com/private/2017/win/132.html')

# View available forms
#for f in br.forms():
#    print f

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=1)

# User credentials
br.form['emailAddress'] = user
br.form['password'] = pwd

# Login
br.submit()


page = (br.open('http://origin.milb.com/private/2016/minor/players/674/477377.html').read())
soup = BeautifulSoup(br.response().read())
tables = soup.findAll("table")

headA = []
statA = []
lineStat =[]
name = soup.findAll('tr')[1]
name = name.find("td")
print name.text

team = soup.findAll("tr")[4]
team = team.find("td")
print team.text

for table in tables:
    theads = table.findAll("thead")
    for thead in theads:
        rows = thead.findAll("tr")
        for row in rows:
            headers = row.findAll("th")
            for head in headers:
                if head.text:
                    headA.append(str(head.text))
            #print headA
            lineStat.append(str(headA))
            del headA[:]
            #print "================================== End row"
    #print "-------------------------------------- end thead"

    tbodies = table.findAll("tbody")
    if len(tbodies)==0:
        rowsTable = table.findAll("tr")
        for rowTable in rowsTable:
            stats = rowTable.findAll("td")
            for stat in stats:
                if stat.text:
                    if stat.text != "*" and stat.text != "#":
                        stat = stat.text.replace(",", "-")
                        stat = stat.replace('\n\t', "")
                        statA.append(str(stat))
            #print statA
            lineStat.append(str(statA))
            del statA[:]

    for tbody in tbodies:
        rowsBody = tbody.findAll("tr")
        for rowBody in rowsBody:
            stats = rowBody.findAll("td")
            for stat in stats:
                if stat.text:
                    if stat.text != "*" and stat.text != "#":
                        stat = stat.text.replace(",", "-")
                        stat = stat.replace('\n\t', "")
                        statA.append(str(stat))
            #print statA
            lineStat.append(str(statA))
            del statA[:]


playerStat = []
for line in lineStat:
    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.replace("'", "")
    line = line.replace(" ", "")
    line = line.split(",")
    if line[0] == "Total":
        total = line[1]
    playerStat.append(line)

for player in playerStat:
    if len(player)>1:
        if player[0]=="DATE" or "1" in player[0]:
            print player
