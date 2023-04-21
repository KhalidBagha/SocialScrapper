from django.shortcuts import render
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import contextlib
import re
from .models import * 


def filter_strings(strings):
    # Regular expressions to match email, phone, and website patterns
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'(\+\d{1,3})?\s?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}'
    website_regex = r"(https?://)?(www\.)?[a-zA-Z0-9]+\.[a-zA-Z]{2,3}(/\S*)?"

    # Create lists to store email, phone, and website matches
    emails = []
    phones = []
    websites = []
    csize=[]

    # Loop through each string in the input list
    for string in strings:
        # Use regular expressions to check for email, phone, and website patterns
        email_match = re.search(email_regex, string)
        phone_match = re.search(phone_regex, string)
        website_match = re.search(website_regex, string)

        # If the string matches an email pattern, add it to the emails list
        if email_match:
            emails.append(email_match.group())

        # If the string matches a phone pattern, add it to the phones list
        elif phone_match:
            phones.append(phone_match.group())

        # If the string matches a website pattern, add it to the websites list
        elif website_match:
            websites.append(website_match.group())
        else:
            m = string.replace("(",'').replace(")",'').replace(" ",'').replace("+",'')
            if m.isnumeric():
                phones.append(string)
            elif '.' in string[-7:-1] and not '@' in string and len(string) <= 25:
                websites.append(string)
            elif 'employees' in string:
                csize.append(string)

    return emails, phones, websites,csize



def startscrapping(request,email,password,keyword,location,url):

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        browser = webdriver.Chrome()
        
        ## login details ## 

        browser.get("https://www.linkedin.com")
        time.sleep(3)
        try:
            emailInp = browser.find_element(By.ID,"session_key")
            passInp = browser.find_element(By.ID,"session_password")
            emailInp.send_keys(email)
            passInp.send_keys(password)

            loginbtn = browser.find_element(By.XPATH, "/html/body/main/section[1]/div/div/form/div[2]/button")
            loginbtn.click()
        except:
            return 


        currUrl = url
        browser.get(currUrl)
        time.sleep(5)
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(8)
        urls = [currUrl]
        ul = browser.find_element(By.CSS_SELECTOR,"ul.artdeco-pagination__pages.artdeco-pagination__pages--number")
        li = ul.find_elements(By.TAG_NAME,'li')[-1].text
        urls = [f"{currUrl}&page={i}"  for i in range(1,int(li)+1)]
        print(urls)
        dictionary = {}
        try:
            for url in urls:
                try:
                    print(url)
                    browser.get(url)
                    time.sleep(5)
                    mainSearchCon = browser.find_element(By.CSS_SELECTOR, "ul.reusable-search__entity-result-list")
                    lis = mainSearchCon.find_elements(By.CSS_SELECTOR,".reusable-search__result-container")
                    
                    for li in lis:
                        mbl = li.find_element(By.CSS_SELECTOR,'div.entity-result__content.entity-result__divider')
                        anchor = mbl.find_element(By.CLASS_NAME,"app-aware-link")
                        jobtitle=""
                        loc=""
                        try:
                            jobtitle= mbl.find_element(By.CSS_SELECTOR,"div.entity-result__primary-subtitle").text
                            loc= mbl.find_element(By.CSS_SELECTOR,"div.entity-result__secondary-subtitle").text
                        except:
                            pass
                        a=anchor.get_attribute("href")
                        jobtitle = jobtitle.split('•')
                        dictionary[a] = [anchor.text,loc]+jobtitle

                        
                    for link,values in dictionary.items():
                                try:
                                    try:
                                        browser.get(link+"about")
                                    except:
                                        continue
                                    time.sleep(4)  
                                    mainDiv = browser.find_element(By.CSS_SELECTOR,".org-grid__content-height-enforcer")
                                    try:
                                        abt = mainDiv.find_element(By.CSS_SELECTOR,"p.break-words").text
                                    except: 
                                        abt = ""
                                    print(abt)
                                    print()
                                    print()
                                    print()
                                    print()

                                    m  =  mainDiv.find_element(By.CSS_SELECTOR,"dl.overflow-hidden").text
                                    m = m.split('\n')
                                    emails, phones, websites,csize = filter_strings(m)
                

                                
                                    Linkedin = Linkedin_Pages.objects.create(
                                        title = values[0],
                                        website = ','.join(websites),
                                        about = abt,
                                        audience = values[1],
                                        link = link,
                                        email = ','.join(emails),
                                        phone = ','.join(phones),
                                        csize = csize,
                                        keyword = keyword,
                                        location = location,
                                        category = values[2]
                                    )

                                    Linkedin.save()
                                
                                    
                                    divs=browser.find_element(By.CSS_SELECTOR,"div.mt1")
                                    a = divs.find_element(By.TAG_NAME,"a")
                                    peoplelink = a.get_attribute("href")
                                    # get employees page link
                                    browser.get(peoplelink) 
                                    time.sleep(10)
                                    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                                    currurl= peoplelink
                                    time.sleep(4)
                                    print("Current URL",peoplelink)
                                    urls = [peoplelink]
                                    try:
                                        ul = browser.find_element(By.CSS_SELECTOR,"ul.artdeco-pagination__pages.artdeco-pagination__pages--number")
                                        li = ul.find_elements(By.TAG_NAME,'li')[-1].text
                                        urls = [f"{peoplelink}&page={i}"  for i in range(1,int(li)+1)]
                                    except:
                                        pass
                                    print("\n--Employee Pagination URLS ---",urls)
                                    
                                    profileLinks = []  #saving each emoloyee profile link to iterate in future
                                    for url in urls:
                                        browser.get(url)
                                        time.sleep(3)
                                        mainSearchCon = browser.find_element(By.CLASS_NAME, "reusable-search__entity-result-list")
                                        lis = mainSearchCon.find_elements(By.CSS_SELECTOR,".reusable-search__result-container")
                                        for li in lis:
                                            div= li.find_element(By.CSS_SELECTOR,".entity-result__title-text")
                                            anchor = div.find_element(By.TAG_NAME,"a")
                                            profileLinks.append(anchor.get_attribute('href'))
                                            
                                    print("\n---Employee Profliles---",profileLinks)

                                    for url in profileLinks:
                                        
                                            browser.get(url)
                                            time.sleep(3)
                                            try:
                                                mainDiv = browser.find_element(By.CSS_SELECTOR,".pv-top-card")

                                                name = mainDiv.find_element(By.TAG_NAME,"h1").text
                                                tag = mainDiv.find_element(By.CSS_SELECTOR,"div.text-body-medium.break-words").text
                                                loc = mainDiv.find_element(By.CSS_SELECTOR,"div.pv-text-details__left-panel.mt2").find_element(By.CSS_SELECTOR,"span.text-body-small.inline.t-black--light.break-words").text
                                                try:    
                                                    ul= mainDiv.find_element(By.CSS_SELECTOR,"ul.pv-top-card--list").find_element(By.CSS_SELECTOR,"span.t-bold").text
                                                except:
                                                    ul=""

                                                section = browser.find_elements(By.CSS_SELECTOR,"section.artdeco-card.ember-view.relative.break-words.pb3.mt2")
                                                for sections in section:
                                                    try:
                                                        currexp = sections.find_element(By.ID,"experience")
                                                        li = sections.find_element(By.TAG_NAME,"li")
                                                        position = li.find_element(By.CSS_SELECTOR,"span.mr1.t-bold").find_element(By.TAG_NAME,"span").text
                                                        types = li.find_element(By.CSS_SELECTOR,"span.t-14.t-normal").find_element(By.TAG_NAME,"span").text
                                                        period = li.find_element(By.CSS_SELECTOR,"span.t-14.t-normal.t-black--light").find_element(By.TAG_NAME,"span").text
                                                        break
                                                    except:
                                                        position=""
                                                        period=""
                                                        types=""
                                                print(name,tag,loc)
                                                print(position,types,period)

                                                print(Linkedin.id,Linkedin)
                                                
                                                Linkedin_emp = Linkedin_Emp.objects.create(
                                                        company = Linkedin,
                                                        name = name,
                                                        tag = tag,
                                                        keyword = keyword,
                                                        location= location,
                                                        jobType = types,
                                                        position = position,
                                                        timePeriod = period,
                                                        link = url 
                                                    )
                                                Linkedin_emp.save()
                                            except:
                                                continue            
                                except:
                                        continue                
                except:
                        continue                    
        except: 
            pass                              
                        
        return render(request,'linkedin/startscrapln.html' )
    
                                    
                    





def create(request):

    if request.method == 'POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            keyword=request.POST.get('keyword')
            location=request.POST.get('location')
            url=request.POST.get('url')

            startscrapping(request,email,password,keyword,location,url)

    return render(request,'linkedin/startscrapln.html' )




def linkedin(request):
    ln_co = Linkedin_Pages.objects.all().order_by('-id').values()
    ln_emp = Linkedin_Emp.objects.all().order_by('-id').values()
    context = {
         'ln_co':ln_co,
         'ln_emp':ln_emp
    }
    return render(request,'linkedin/linkedinWhole.html',context )



def sendmessage(request,pk):

    emp = Linkedin_Emp.objects.get(id = pk)

    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        message = request.POST.get('message')

        if '@username' in message:
            message = message.replace('@username',str(emp.name))
        else:
            message = message

        if message != '':
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            browser = webdriver.Chrome()

            browser.get("https://www.linkedin.com")
            time.sleep(3)
            try:
                emailInp = browser.find_element(By.ID,"session_key")
                passInp = browser.find_element(By.ID,"session_password")
                emailInp.send_keys(email)
                passInp.send_keys(password)

                loginbtn = browser.find_element(By.XPATH, "/html/body/main/section[1]/div/div/form/div[2]/button")
                loginbtn.click()
            except:
                return False

            browser.get(emp.link)
            time.sleep(10)

            try:
                browser.find_element(By.CSS_SELECTOR,'.pvs-profile-actions').find_elements(By.TAG_NAME,'button')[0].click()
                time.sleep(5)
                browser.find_element(By.CSS_SELECTOR,'button[aria-label="Add a note"]').click()
                time.sleep(2)
                browser.find_element(By.ID,'custom-message').send_keys(message)
                time.sleep(2)
                browser.find_element(By.CSS_SELECTOR,'button[aria-label="Send now"]').click()
                print("Message Sent")
            except:
                try:   
                    browser.find_element(By.CSS_SELECTOR,'div[aria-label="Write a message…"]').send_keys(message)
                    time.sleep(2)
                    browser.find_element(By.XPATH,'/html/body/div[5]/aside/div[2]/div[2]/form/footer/div[2]/div[1]/button').click()
                    print("Message Sent")
                    time.sleep(3)
                except:
                    pass

            

    return render(request,'linkedin/message.html',{'id':pk} )

