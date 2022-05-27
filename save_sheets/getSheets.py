# connects to db
import mysql.connector
import requests

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mas_sheets"
)
mycursor = mydb.cursor()

# get all the link of the sheets
def getAllLink(mycursor):

    # Checks if data is already available or not
    sql = "SELECT * FROM links WHERE status = 'active'"
    mycursor.execute(sql,)
    links = mycursor.fetchall()
    return links


# get all the data from the
def saveSheets(sheet):
    response = requests.post('https://server.myauctionsheet.com/auction/save-sheets', data=sheet).json()

    if not response['error']:
        print(response['message'])
        return 1
    else:
        print(response['message'])
        return 0


# inactive the current link
def inactiveLink(link, mycursor):
    sql = "UPDATE links set status = 'inactive' where link = %s"
    mycursor.execute(sql, (link,))
    mydb.commit()