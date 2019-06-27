"""
-Google adwords automated bot-

Created by Manos Liakos. All rights reserved 2019.



*** This bot receives as input a list of domains that are used in Google Adwords campaign and keywords for each one of them and runs infinitely until the ad budget for the selected keywords has been depleted. ***

It uses selenium webdriver (regular browser) to scrape ad URLs for each keyword-domain combination and saves them in an array.
Then TOR browser is used to simulate a real visit to the URL, using a different IP address each time. Every time, after executing all visits
a new search is performed for each domain stacking the array with URLs and requests are done to every URL in the array including the old ones.
That happens because they don't expire (meaning they still charge the victim, so damage is done in less time :D). The script runs in a loop and each time 
a certain domain is not found using the selected keywords, it gets removed from the array. Once the array has been emptied, the script is run 4 additional 
times to ensure that the ad budget for each domain-keyword combo has been indeed depleted.


"""


from selenium import webdriver
from tbselenium.tbdriver import TorBrowserDriver
from torrequest import TorRequest
import time, os, requests, datetime, socket

TESTING = False
########################################## Functions Start ##########################################

# Check connection
REMOTE_SERVER = "www.google.com"
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def checkConn():
    while(True):
        if(is_connected(REMOTE_SERVER) == False):
            print('Network error occured. Rechecking connection in 5 seconds...')
            time.sleep(5)
        else:
            break

def googleSearch(keyword, driver):
    """
    Takes keyword as argument. Focuses on search input, clears it and perform a search.
    """
    checkConn()
    
    #Clearing search input
    driver.find_element_by_css_selector('.gLFyf').clear()
    
    # Focusing on search input
    driver.find_element_by_css_selector('.gLFyf').click()

    #Typing keyword or phrase in search input
    driver.find_element_by_css_selector('.gLFyf').send_keys(keyword)

    #Pressing enter
    driver.find_element_by_css_selector('.gLFyf').send_keys(u'\ue007')

def parseResults(domain, driver):
    """
    Parses page for ads. Takes wanted domain as argument. (type: str)
    If ad is found, {domain:url} object gets appended to URLs array, if it doesn't exist. 
    If it does, url is appended to URLs' array domain object.
    """
    #Get all ads
    ads = driver.find_elements_by_class_name('ads-visurl')

    # Initializing counter
    counter = 0

    # If there are any ads
    if(len(ads) != 0):
        # Add to array if wanted domain #

        # For every ad found
        for ad in ads:
            if(domain in ad.text):

                ### For testing purposes only ###
                if TESTING == True:
                    if '10 λεπτά' in ad.find_element_by_xpath('preceding-sibling::h3').text:
                        #Increment counter by one
                        counter += 1
                        # Getting ad url
                        url = ad.find_element_by_xpath('../../a').get_attribute('href')

                        #If array is empty append first object
                        if(len(URLs) == 0):
                            URLs.append({domain:[url]})
                        else:                
                            #Checking if domain object exists
                            for obj in URLs:
                                #Domain does not exist
                                if(domain not in obj):
                                    URLs.append({domain:[url]})
                                #Domain already exists
                                else:
                                    obj[domain].append(url)
                else:
                    #Increment counter by one
                    counter += 1
                    # Getting ad url
                    url = ad.find_element_by_xpath('../../a').get_attribute('href')

                    #If array is empty append first object
                    if(len(URLs) == 0):
                        URLs.append({domain:[url]})
                    else:                
                        #Checking if domain object exists
                        for obj in URLs:
                            #Domain does not exist
                            if(domain not in obj):
                                URLs.append({domain:[url]})
                            #Domain already exists
                            else:
                                obj[domain].append(url)
    
    return counter

def makeRequest(url, domain):
    """
    Makes HTTP request to url given as argument, after changing IP.
    """
    import time
    



    # Opening log file
    f = open(logfile_name, 'a')

    print('Changing IP...\n')
        
    # Below is method A using requests library without opening real TOR browser.
    # Method B will be used instead, which opens a real browser, so that JS code is executed
    # and Google Analytics tracks us as a real user.

    """
    # Resetting IP
    tr.reset_identity()
    # This command changes restarts tor service, resulting in IP address change. After '-p' flag insert user password.
    #os.system('sudo systemctl restart tor -p 0000')

    #Creating empty session object
    session = requests.session()
    session.proxies = {}

    # Adding proxies to session
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    #Changing request headers
    headers = {}
    headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    print('Request headers were set.\n') 
-
    new_ip = session.get('http://ipecho.net/plain').text
    

    # Executing requests 

    #Executing request and assigning response status code
    status_code = session.get(url).status_code
    """

    
    # Method B, using complete TOR Browser

    driver = TorBrowserDriver("/home/manos/Desktop/tor-browser_en-US")
    # driver.get('https://ipecho.net/plain')
    # new_ip = driver.find_element_by_tag_name('body').text

    checkConn()

    driver.get(url)
    time.sleep(2.0)
    driver.close()

    # Request logging
    time = 'Date: ' + str(datetime.datetime.now())[0:10] + '\nTime: ' + str(datetime.datetime.now())[11:19] 
    f.write(

    time +'\nDomain: ' + domain + '\n'
    'Request sent to ' + url + '.' + '\nResponse status code: ' + str(200) + '\n*******************************************************************************************\n\n'

    )
    f.close()
    os.system('clear')




########################################## Functions End ##########################################

########################################## Script Initialization Start ##########################################
targets = [] # {'Domain':[Keywords]}
targets_backup = []
URLs = [] # {'Domain':[Urls]}

while(True):
    while(True):
        os.system('clear')
        domain = input('\nEnter domain: (i.e. google.com)\n')
        if('.' in domain):
            break
        else:
            os.system('clear')
            print('\nPlease enter a valid domain!')
    

    keywords = input('Enter keywords for selected domain (' + domain +'). Separate with comma and a whitespace (i.e. foo, bar, foobar).\n').split(', ')
    
    # Creating targets list
    targets.append({'domain':domain,'keywords':keywords})
    
    # Creating backup list
    targets_backup.append({'domain':domain,'keywords':keywords})

    if(input('Do you want to add another domain? (y/n)\n') == 'y'):
        pass
    else:
        os.system('clear')
        print('Entered info:\n')
        for num, target in enumerate(targets):
            print('\n' + str(num+1) +'. ' + target['domain'] + ', ' + str(target['keywords']) + '\n' )
        print('Script started.')
        break

########################################## Script Initialization End ##########################################

########################################## Gathering Ad URLs Start ##################################################
def main():
    global round_counter

    # Performing search for each target
    for index,target in enumerate(targets):

        # Performing search for each keyword
        for keyword in target['keywords']:
            counter = 0
            # Opening webdriver
            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

            checkConn()

            driver.get('https://google.com')

            #Performing search
            googleSearch(keyword, driver)

            # Parsing first page for ads
            counter += parseResults(target['domain'], driver)

            # Get all pages length
            pages_len = len(driver.find_elements_by_css_selector('#nav > tbody > tr > td'))-2

            try:
                # Loop through pages
                for i in range(1,pages_len):
                    checkConn()
                    page = driver.find_elements_by_css_selector('#nav > tbody > tr > td')[i]
                    # Excluding 
                    if(page.get_attribute('class')!= 'cur'):
                        page.click()

                        # Parsing first page for ads
                        counter += parseResults(target['domain'], driver)
            except IndexError:
                print('Pages were changed during iteration. Script will continue with next keyword/domain.\n')

            print('Found ' + str(counter) + ' ads for domain \'' + target['domain'] + '\' and keyword \'' + keyword + '\'.\n')

            # For each target 
            for target in targets:
                # For object ({domain:URLs array}) 
                for obj in URLs:
                    # Checking if domain exists at all
                    if(target['domain'] in obj):
                        # For each domain's url 
                        for url in obj[target['domain']]:
                            # Execute request 
                            makeRequest(url, target['domain'])
                            round_counter += 1
                            print(URLs)
                            print(targets)

            #Closing webdriver
            driver.close()
        
        try:
            # Get domain URLs count
            total_length = [len(item[target['domain']]) for item in URLs if item[target['domain']]][0] 

        except: #KeyError or IndexError
            # Domain not in array (length == 0)
            total_length = 0
            if(len(targets) > 0):
                del targets[index]
                print('Target was removed from list.')
        print('Found ' + str(total_length) + ' ads in total for domain \'' + target['domain'] +'\'.\n')
    
    

########################################## Gathering Ad URLs End ##################################################

########################################## Clicking Start ##################################################

# Setting up TOR
#tr=TorRequest(password='0000')

# current_ip = requests.get('http://ipecho.net/plain').text

# print('\n\nCurrent IP: ' + current_ip + '\n')
round_counter = 1

#Logfile
logfile_name = str(time.time()).split('.')[0]+'.txt'

global_counter = 1

while(len(targets) > 0):
    print('Round ' + str(round_counter))
    main()
else:
    while(global_counter <= 4):
        print('\nNo ads found. Performing additional runs. Run number ' + str(global_counter) + ' \n')
        targets = targets_backup.copy()
        print('Round ' + str(round_counter))
        main()
        global_counter += 1

print('\nScript was terminated.\n')
    

########################################## Clicking End ##################################################




