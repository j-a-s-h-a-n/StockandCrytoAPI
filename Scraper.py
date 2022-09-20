import requests
from bs4 import BeautifulSoup


def getStock(tag):
        tag=tag.replace('^','%5E').upper()
        url = 'https://finance.yahoo.com/quote/' + tag
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            name = soup.find("h1",{'class':'D(ib) Fz(18px)'}).text
            price = soup.find("fin-streamer",{'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
            previous_close_price = soup.find("td",{'class':'Ta(end) Fw(600) Lh(14px)',
                                                       'data-test':'PREV_CLOSE-value'}).text
            open_price = soup.find("td",{'class':'Ta(end) Fw(600) Lh(14px)',
                                                 'data-test':'OPEN-value'}).text
            price_change = soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text
            low_high_24=  soup.find("td",{'class':'Ta(end) Fw(600) Lh(14px)',
                                                       'data-test':'DAYS_RANGE-value'}).text
            trading_volume = soup.find("td",{'class':'Ta(end) Fw(600) Lh(14px)',
                                                       'data-test':'TD_VOLUME-value'}).text
            #market_cap = soup.find("td",{'class':'Ta(end) Fw(600) Lh(14px)',
                                                       #'data-test':'MARKET_CAP-value'}).text
        except:
            return {'Message':'Stock not found in our database.'}
        return {
            'Name':name,
            'Price': price,
            'Price Change': price_change,
            '24 Hour Low and High': low_high_24,
            'Previous Closing Price': previous_close_price,
            'Open Price': open_price,
            'Trade Volume': trading_volume,
            #'Market Cap': market_cap
        }
def getCrypto(name):
        name = name.replace(' ', '-').upper()
        name = name.replace('.', '-')
        url = 'https://coinmarketcap.com/currencies/'+name
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            price= soup.find('div', {'class':'sc-16r8icm-0 fmPyWa',
                                     }).find_all('td')[0].text
            price_change= soup.find('div', {'class':'sc-16r8icm-0 fmPyWa',
                                     }).find_all('td')[1].text[:-5]
            low_high_24= soup.find('div', {'class':'sc-16r8icm-0 fmPyWa',
                                     }).find_all('td')[2].text
            trading_volume= soup.find('div', {'class':'sc-16r8icm-0 fmPyWa',
                                     }).find_all('td')[3].text[:-6]
            #market_cap  = soup.find('div', {'class':'sc-16r8icm-0 nds9rn-0 dAxhCK',
                                     #}).find_all('td')[7].text[:-5]
            market_rank= soup.find('div', {'class':'sc-16r8icm-0 fmPyWa',
                                     }).find_all('td')[6].text
            market_dom= soup.find('div', {'class':'sc-16r8icm-0 fmPyWa',
                                     }).find_all('td')[5].text
        except:
            return {'Message' : 'Cryptocurrency not found in our database.'}
        return {
            'Name': name,
            'Price': price[1:],
            'Price Change': price_change.replace('$',''),
            '24 Hour Low and High': low_high_24.replace('$','').replace('/','- '),
            'Trade Volume': trading_volume.replace('$',''),
            #'Market Cap': market_cap.replace('$',''),
            'Market Rank': market_rank,
            'Market Dominance': market_dom
        }
def getStockStat(tag):
    tag = tag.replace('^', '%5E').upper()
    url = 'https://finance.yahoo.com/quote/' + tag
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find("fin-streamer", {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    price_change = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text
    return {
        'Price': price,
        'Price Change': price_change
    }

def getCryptoStat(name):
    name = name.replace(' ', '-').upper()
    name = name.replace('.', '-')
    url = 'https://coinmarketcap.com/currencies/' + name
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('div', {'class': 'sc-16r8icm-0 fmPyWa',
                                      }).find_all('td')[0].text
    price_change = soup.find('div', {'class': 'sc-16r8icm-0 fmPyWa',
                                             }).find_all('td')[1].text[:-5]
    return {
            'Price': price,
            'Price Change': price_change,
        }