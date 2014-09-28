
import urllib2, re, urlparse
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime


html = urllib2.urlopen("http://www.eastlothian.gov.uk/site/custom_scripts/foi_download_index.php?currentPage=1&itemsPerPage=2000000").read()

datePattern = r'(January|February|March|April|May|June|July|August|September|November|December) 20[0-9][0-9]$'
idPattern = r'^http://www.eastlothian.gov.uk/download/downloads/id/(?[0-9]+)/.*$'
soup = BeautifulSoup(html)

rows = soup.table.findAll('tr')

for x in range(1, len(soup.table.findAll('tr'))):

        cnx = mysql.connector.connect(user='foiawiki', password='579dVZq8BBa3XRcc', database='foiawiki')

        cols = rows[x].findAll('td')
        if ( re.search(datePattern, cols[0].string) is not None ):
            title = re.sub(datePattern, '', cols[0].string).strip()
            if title[-1] == '-':
                title = title[:-1].strip()
            date = re.search(datePattern, cols[0].string).group(0)
            iden = urlparse.urlparse(cols[0].a['href']).path.split('/')[4]
            tags = [re.sub(r'^the', '', tag).lower().strip() for tag in cols[3].string.split(" and ")]

            tags.append('east lothian')

            cursor = cnx.cursor()

            query = "SELECT * FROM request WHERE publicBodyId = 2 AND requestId = %s"
            cursor.execute(query, (iden,))
            if cursor.fetchone() != None:
                print "ROW RETURNED!"
                cursor.close()
                continue

            timestamp = datetime.strptime(date, "%B %Y")
            query = "INSERT INTO request VALUES (%s, %s, NULL, %s, %s, %s, NULL)" 

            cursor.close()
            cnx.close()
            cnx = mysql.connector.connect(user='foiawiki', password='579dVZq8BBa3XRcc', database='foiawiki')
            cursor = cnx.cursor()
            cursor.execute(query, ('2', iden, title, timestamp, cols[0].a['href']))
            for tag in tags:
                cursor.execute("INSERT INTO requestTag VALUES (%s, %s)", (iden, tag))
            cnx.commit()
            cursor.close()
        

            print "ID: %s" % (iden,)
            print "Title: %s" % (title,)
            print "Date: %s" % (date,)
            print "PDF URL: %s" % (cols[0].a['href'],)
            print "Tags: %s" % (tags,)
            print "----------------------------------------------------"

