from django.shortcuts import render
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import contextlib
import re
from .models import * 
from selenium.webdriver.common.keys import Keys



## FaceBook pages





def Fblogin(request,browser,email,password):
    browser.get("https://www.facebook.com/login/")
    time.sleep(3)
    with contextlib.suppress(NoSuchElementException):
        browser.find_element(By.CLASS_NAME,"_1kbt").send_keys(email)
        browser.find_element(By.CLASS_NAME,"_9npi").send_keys(password)
        browser.find_element(By.ID, "loginbutton").click()
        return True
    return False
    


def filter_strings(strings):
    # Regular expressions to match email, phone, and website patterns
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'(\+\d{1,3})?\s?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}'
    website_regex = r"(https?://)?(www\.)?[a-zA-Z0-9]+\.[a-zA-Z]{2,3}(/\S*)?"
    address_regex = r"^[A-Za-z0-9\s#.,\-\/&'()]+$"

    # Create lists to store email, phone, and website matches
    emails = []
    phones = []
    websites = []
    ratings = []
    address = []

    # Loop through each string in the input list
    for string in strings:
        # Use regular expressions to check for email, phone, and website patterns
        email_match = re.search(email_regex, string)
        phone_match = re.search(phone_regex, string)
        website_match = re.search(website_regex, string)
        address_match = re.search(address_regex, string)

        # If the string matches an email pattern, add it to the emails list
        if email_match:
            emails.append(email_match.group())

        # If the string matches a phone pattern, add it to the phones list
        elif phone_match:
            phones.append(phone_match.group())

        # If the string matches a website pattern, add it to the websites list
        elif website_match:
            websites.append(website_match.group())

        elif address_match:
            address.append(address_match.group())
        
        else:
            m = string.replace("(",'').replace(")",'').replace(" ",'').replace("+",'')
            if m.isnumeric():
                phones.append(string)
            elif '.' in string[-7:-1] and not '@' in string and len(string) <= 25:
                websites.append(string)
            elif ("rating" or "rate") in string:
                ratings.append(string)
                
            

    return emails, phones, websites,ratings,address



def setFbFilters(request,browser,keyword,location):
    try:
        time.sleep(3)
        browser.get("https://www.facebook.com/search/pages/?q="+keyword)
        time.sleep(5)
        browser.find_element(By.CSS_SELECTOR,"div.x9f619.x78zum5.xurb0ha.x1y1aw1k.xwib8y2.x1yc453h.xh8yej3").click()
        time.sleep(5)
        ## adding location filter
        browser.execute_script("document.querySelector(\"input[placeholder='Choose a City...']\").style.display = 'block';")
        input_element = browser.find_element(By.CSS_SELECTOR,"input[placeholder='Choose a City...']")
        time.sleep(8)
        input_element.send_keys(location)
        time.sleep(8)
        browser.find_element(By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]").click()

    except:
         pass
         

def scrollToBottom(request,browser):
    prevHeight = browser.execute_script('return document.body.scrollHeight')

    while True:
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new = browser.execute_script('return document.body.scrollHeight')
        print("Scrolling down...")
        if new == prevHeight:
            break
        prevHeight = new

def datascrapping(request,browser,keyword,location):
    try:
    
        mainDiv = browser.find_element(By.CLASS_NAME,"x1xwk8fm")  ## main articles div - > pages div
        articles = mainDiv.find_elements(By.CLASS_NAME,"x1yztbdb") ## list of pages 
        urls = []
        data = {}

        for i in articles:  ## iterating through each page 
            try:
                    titlediv = i.find_element(By.CSS_SELECTOR,"span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.xk50ysn.xzsf02u.x1yc453h")
                    title= titlediv.text  # name of page 
            except:
                title=""
            try:    
                    anch = titlediv.find_element(By.TAG_NAME,"a").get_attribute('href')  # url of page 
                    urls.append(anch)
            except:
                anch=''
            try:
                    details = i.find_element(By.CSS_SELECTOR,"span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6")
                    dm=details.text.split("·")
                    try:
                            dm.remove("Open now ")
                    except: 
                            pass
                    try:
                            dm.remove(" Open now ")
                    except: 
                            pass

                    try:
                            dm.remove("Open Soon  ")
                    except: 
                            pass
                    try:
                            dm.remove("$$$ ")
                    except: 
                            pass
                    try:
                            dm.remove("$$ ")
                    except: 
                        pass
                    try:
                            dm.remove("$ ")
                    except: 
                        pass

                    try:
                            dm.remove("$$$$ ")
                    except: 
                        pass
                    try:
                            dm.remove(' Always open ')
                    except:
                            pass
                    try:
                        dm.remove(' 10+ posts in the last 2 weeks')
                    except:
                        pass
                    try:
                        dm.remove(' Closed now ')
                    except:
                        pass

                    cat  = dm[0]
                    if len(dm) == 3:
                        rate=dm[1]
                        audience=dm[2]
                    elif len(dm)==4:
                        rate=dm[1]
                        audience=dm[2]
                    elif len(dm)==2:
                        cat= dm[0]
                        rate=""
                        audience=dm[1]
                    else:
                        rate=""
                        audience=""
            except:
                        cat= ""
                        rate=""
                        audience=""
            try:
                    about = i.find_element(By.CSS_SELECTOR,"span.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84").text
            except:
                about=""
                
                
            data[anch] = [title,about,cat,rate,audience]  # url : [name,about,category,rating,followers/likes] 
        



        for key,val in data.items():

            try:
                browser.get(key)
                time.sleep(3)
                x=browser.find_element(By.CSS_SELECTOR,".x9f619.x1n2onr6.x1ja2u2z.x2bj2ny.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.xh8yej3.x6ikm8r.x10wlt62.xquyuld").text
                m=x.split('\n')
                email,phone,web,rat,adr = filter_strings(m)
                audience  = ""
                with contextlib.suppress(NoSuchElementException):
                    audience = browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]").text
                if len(rat) < 1:
                    rat = val[3]
                else:
                    rat = ','.join(rat)
                print(key,val[0],val[1],val[2],email,phone,web,rat,audience)
                
                try:
                    x = Facebook_Pages.objects.create(
                        title =  val[0],
                        link = key, 
                        about = val[1], 
                        audience = audience, 
                        rating = rat, 
                        category = val[2], 
                        keyword = keyword, 
                        location = location, 
                        email = '-'.join(email), 
                        phone = '-'.join(phone), 
                        website = '-'.join(web), 
                        )
                    x.save()
                except :
                    print("Error ->",anch)
                    continue
            except:
                continue
    except:
         pass

def startscrapping(request,email,password,keyword,location):    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(options=options)
    Fblogin(request,browser,email,password)
    setFbFilters(request,browser,keyword,location)
    scrollToBottom(request,browser)
    datascrapping(request,browser,keyword,location)

    return render(request,'facebook/facebookWhole.html')




def create(request):

    if request.method == 'POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            keyword=request.POST.get('keyword')
            location=request.POST.get('location')

            startscrapping(request,email,password,keyword,location)

    return render(request,'facebook/startscrap.html' )




def facebook(request):
    fb = Facebook_Pages.objects.all().order_by('-id').values()
    context = {
         'fb':fb
    }
    return render(request,'facebook/facebookWhole.html',context )

def FbMessage(request,browser,message,my_field_list):
            for i in my_field_list:
                try:
                    if '@username' in message:
                        message = message.replace('@username',str(i))
                    else:
                        message = message   

                    browser.get("https://www.facebook.com/messages/t")
                    time.sleep(8)
                    x= browser.find_element(By.CSS_SELECTOR,"input[placeholder='Search Messenger']")
                    x.send_keys(i)
                    time.sleep(5)
                    li = browser.find_elements(By.CSS_SELECTOR,"li.xexx8yu.xsyo7zv.x18d9i69.x16hj40l")
                    li=li[1]
                    n="div x6s0dn4 x1ypdohk x78zum5 x6ikm8r x10wlt62 x1n2onr6 x1lq5wgf xgqcy7u x30kzoy x9jhf4c xdj266r xat24cr x1y1aw1k x1sxyh0 xwib8y2 xurb0ha x8du52y".replace(' ','.')
                    x=li.find_elements(By.CSS_SELECTOR,n)
                    x[0].click()
                    # m = "a x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1rg5ohu x1a2a7pz xh8yej3".replace(' ','.')
                    # a=browser.find_element(By.CSS_SELECTOR,m).click()
                    time.sleep(5)
                    m=browser.find_element(By.CSS_SELECTOR,".notranslate").send_keys(message+Keys.ENTER)
                    time.sleep(5)
                except:
                    continue 
            return render(request,'facebook/message.html')


def sendmessagewindow(request,email,password,keyword,message):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(options=options)

    queryset = Facebook_Pages.objects.filter(keyword__icontains=keyword)
    my_field_values = queryset.values_list('title', flat=True)
    my_field_list = list(my_field_values)

    Fblogin(request,browser,email,password)
    FbMessage(request,browser,message,my_field_list)

    return render(request,'facebook/facebookWhole.html')


def sendmessage(request):
     if request.method == "POST":
            email=request.POST.get('email')
            password=request.POST.get('password')
            keyword=request.POST.get('keyword')
            message=request.POST.get('message')

            sendmessagewindow(request,email,password,keyword,message)

     return render(request,'facebook/message.html')