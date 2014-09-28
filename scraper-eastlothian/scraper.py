
import urllib2, re, urlparse
from bs4 import BeautifulSoup
import mysql.connector

cnx = mysql.connector.connect(user='foiawiki', password='579dVZq8BBa3XRcc', database='foiawiki')

html = urllib2.urlopen("http://www.eastlothian.gov.uk/site/custom_scripts/foi_download_index.php?currentPage=1&itemsPerPage=2000000").read()

datePattern = r'(January|February|March|April|May|June|July|August|September|November|December) 20[0-9][0-9]$'
idPattern = r'^http://www.eastlothian.gov.uk/download/downloads/id/(?[0-9]+)/.*$'
soup = BeautifulSoup(html)

rows = soup.table.findAll('tr')

for x in range(1, len(soup.table.findAll('tr'))):
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

            query = "SELECT * FROM request WHERE `publicBodyId` = 2 AND `requestId` = %d"
            cursor.execute(query, (iden))
            if cursor.rowcount > 0:
                cursor.close()
                continue

            query = "INSERT INTO request VALUES (%s, %s, NULL, %s, %s, %s, NULL)"

            timestamp = datetime.strptime(date, "%B %Y")

            cursor.execute(query, (2, iden, title, timestamp, cols[0].a['href']))

            print "ID: %s" % (iden,)
            print "Title: %s" % (title,)
            print "Date: %s" % (date,)
            print "PDF URL: %s" % (cols[0].a['href'],)
            print "Tags: %s" % (tags,)
            print "----------------------------------------------------"

