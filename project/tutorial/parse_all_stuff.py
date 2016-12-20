import urllib2
from bs4 import BeautifulSoup
import re

# function div_generator
def page_grab(url):
    page_url = url
    page_soup = BeautifulSoup(urllib2.urlopen(page_url).read(), 'html.parser')
    page_products = page_soup.findAll('div', {'class':'g-i-tile g-i-tile-catalog'})
    return page_products

# function for getting price
def price_grab(div):
    price_block = div.find('div', {'name':'prices_active_element_original'})
    script = price_block.find('script')
    price = re.findall('".+?3A([0-9]+)', str(script))
    
    if price == []:
        price_block = div.find_all('div', {'name':'prices_active_element_original'})
        script = price_block[1].find('script')
        price = re.findall('".+?3A([0-9]+)', str(script))
        return int(price[0])
    
    return int(price[0])

# function for cleaning data
def div_grab(divs):
    complited_data = []
    for div in divs:
        title_div = div.find('div', {'class':'g-i-tile-i-title'})
        title_a = title_div.find('a')
        # name
        name = title_a.get_text().replace('\n', '').replace('\t', '')
        # link
        link = title_a['href']
        # image
        image_div = div.find('div', {'class':'g-i-tile-i-image'})
        image_tag = image_div.find('img')
        image = image_tag['data_src']
        # price (don't forget 'bout spaces removing)
        price = price_grab(div)
        
        # bonus
        exist = image_div.find('i')
        if exist is None:
            bonus = "Out of stock"
        elif u'g-tag-icon-middle-superprice' in exist['class']:
            bonus = 'Superprice'
        elif u'g-tag-icon-middle-action' in exist['class']:
            bonus = 'Action'
        else:
            bonus = False
        
        # complitating 
        data = [name, image, price, bonus, link]
        complited_data.append(data)

    return complited_data

# function for sorting data
def data_sort(data, pricefrom, priceto=False):
    # I TAKE PRICEFROM AND PRICETO!!!
    if priceto == False:
        filtred_data = [item for item in data if item[2] >= int(pricefrom)]
    else:
        filtred_data = [item for item in data if (item[2] >= int(pricefrom))and(item[2] <= int(priceto))]
    ordered_data = sorted(filtred_data, key=lambda item: item[2])
    
    return ordered_data

# main function
def main_function(pricefrom, priceto=False):
    # founding number of pages
    main_url = 'http://rozetka.com.ua/stabilizers/c144719/'
    soup = BeautifulSoup(urllib2.urlopen(main_url).read(), 'html.parser')
    list_of_divs = []
    
    paginator = soup.find('ul', {'name':'paginator'})
    last_page = paginator.find_all('li')[-1]
    num_pages = int(last_page.find('a').get_text())
    
    # Sending main URL in function
    list_of_divs += page_grab(main_url)
    
    # Collecting production from other URLS
    for i in range(2, num_pages+1):
        i_url = main_url + 'page=' + str(i) + '/'
        list_of_divs += page_grab(i_url)
    
    # counting of all divs
    counter = 0
    for div in list_of_divs:
        counter += 1
    
    # sending divs in function
    data = div_grab(list_of_divs)
    
    # sorting and ordering data
    sorted_data = data_sort(data, pricefrom, priceto)
    
    # output
    return sorted_data

# Searching for with some-value of attribute:
# element = soup.find("element(p/div/a)", { "attr(class/id)" : "some-value" })

# Sorting with anonimous function:
# ordered_data = sorted(data, key=lambda item: item[2])