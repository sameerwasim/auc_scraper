from bs4 import BeautifulSoup

# connects to db
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mas_sheets"
)
mycursor = mydb.cursor()

# save to db function
def saveDB(link, mycursor):
    # Checks if data is already available or not
    val = link
    sql = "SELECT * FROM links where link = (%s)"
    mycursor.execute(sql, (val,))
    lenght = mycursor.fetchall()

    if len(lenght) == 0:
        # Inserts into DB
        sql = "INSERT INTO links (link, status) VALUES (%s, %s)"
        mycursor.execute(sql, (val, 'active',))
        mydb.commit()


def findSave(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a.has_attr('href'):
            if '.htm' in a['href']:
                saveDB(a['href'], mycursor)