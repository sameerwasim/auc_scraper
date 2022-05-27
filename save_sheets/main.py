import re
import requests
import datetime
from bs4 import BeautifulSoup
# get all links
from getSheets import getAllLink, mycursor, saveSheets, inactiveLink
links = getAllLink(mycursor)

# required variables
saveSheetCount = 0
skipSheetCount = 0
name = input('Please, Enter your name: ')

for link in links:

    sheet = {}
    imageLink = []

    url = 'http://auc.autodealsjapan.com/'+link[0]

    # get page content
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    try:
        # get Images links
        images = soup.find_all("img")
        for image in images:
            if 'http://8.ajes.com' in image['src']:
                imageLink.append(image["src"].replace('&w=320', ''))

        # get main data
        form = soup.find("form", {'id': 'poisk'})
        sheet['brand'] = form.find('input', {'name': 'manuf_name'})['value']
        sheet['maker'] = form.find('input', {'name': 'model_name'})['value']
        sheet['year'] = form.find('input', {'name': 'year'})['value']
        sheet['condition'] = form.find('input', {'name': 'rate'})['value']
        sheet['chassisCode'] = form.find('input', {'name': 'kuzov_mem'})['value']
        sheet['grade'] = form.find('input', {'name': 'grade'})['value']
        sheet['milleage'] = form.find('input', {'name': 'probeg_hist'})['value']
        sheet['engineCC'] = form.find('input', {'name': 'eng_v_hist'})['value']
        sheet['color'] = form.find('input', {'name': 'colour_hist'})['value']
        # finishPrice = form.find('input', {'name': 'price_finish'})['value']

        # get lot number and auction house
        title = str(re.findall(r"try{document.title='.*';}", str(soup.find_all('script')))[0])
        title = (title.replace("try{document.title='", '').replace("';}", '')).split()

        try:
            lotIndex = title.index(sheet['maker']) + 1
        except Exception:
            title = str(re.findall(r"try{document.title='.*';}", str(soup.find_all('script')))[0])
            title = (title.replace("try{document.title='" + sheet['brand'] + " " + sheet['maker'] + "", '').replace("';}",
                                                                                                                    '')).split()
            lotIndex = 1

        sheet['lotNumber'] = soup.find(class_='vw_top_fix media_v1').text
        auctionHouse = []
        while lotIndex < len(title) - 1:
            lotIndex += 1
            auctionHouse.append(title[lotIndex])
        sheet['auctionHouse'] = ' '.join(auctionHouse)

        # get equipment
        try:
            sheet['equipment'] = soup.find(class_='aj_equip').text
        except Exception:
            sheet['equipment'] = ''

        # get start and finish price
        try:
            price = soup.find('div', {'id': 'Fcurr00'}).text
            price = price.split('|')
            sheet['startPrice'] = price[1]
            sheet['finishPrice'] = price[2]
        except Exception:
            sheet['startPrice'] = 0
            sheet['finishPrice'] = 0

        # get status
        try:
            sheet['status'] = soup.find('div', attrs={
                'style': 'margin-right:2px;font-family:Arial;color:#666;font-size:12px;line-height:12px'}).text
        except Exception:
            sheet['status'] = '-'

        # get transmission
        try:
            transmission = soup.find(class_='aj_equip').parent
            sheet['transmission'] = transmission.find('font', attrs={'style': 'color:#a93f15'}).text
        except Exception:
            sheet['transmission'] = ''

        # get auction date
        try:
            divs = soup.find_all(text=re.compile(sheet['auctionHouse']))
            for div in divs:
                auctionDate = re.findall(r'\d{2}.\d{2}.\d{4}', div.parent.text)
            sheet['auctionDate'] = auctionDate[0]
        except:
            sheet['auctionDate'] = ''

        # get chassis
        print('--------------------------------------------------------------------')
        print("\nAll Images Link: %s" % imageLink)
        printSheetLink = imageLink[-1]
        print("\nExpected Sheet Link: %s " % printSheetLink)
        chassis = input("Enter Chassis No.: (To Stop Enter 'stop' or 'skip' if you wanna move to next one) ")
        print('\n--------------------------------------------------------------------')

        if chassis == 'stop':
            break
        elif chassis == 'skip':
            skipSheetCount += 1
            inactiveLink(link[0], mycursor)
        else:
            sheet['chassis'] = chassis
            sheet['images'] = imageLink
            saveSheetCount += saveSheets(sheet)
            inactiveLink(link[0], mycursor)
    except Exception:
        pass

print('\n %s saved %s sheets on %s' % (name, saveSheetCount, datetime.datetime.now()))
print('\n %s skipped %s sheets on %s' % (name, skipSheetCount, datetime.datetime.now()))
print('\n--------------------------------------------------------------------')
input('\nEnter Q to quit')