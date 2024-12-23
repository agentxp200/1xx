from django.shortcuts import render
from . models import reg,scam,feedback,notifications,scammodel
import random
key="1ccoiAdXjhPLKzq83pmev7bb9mLK6rxt"
link='https://www.ipqualityscore.com/api/json/url/'+key
import requests
from urllib.parse import urlparse
from requests.exceptions import HTTPError
# Create your views here.
def index(request):
    if request.method =='POST':
      url = request.POST.get('link')
      parsed_url=urlparse(url)
      domain=parsed_url.netloc
      print('domain name',domain)

      #scam(urls=url).save()
      return render(request,'register.html')
    else:
      dat=notifications.objects.first() 
      d=dat.data
      return render(request,'index.html',{'data':d})
  
       
def beforelogincheck(request):
    if request.method =='POST':
      url = request.POST.get('link')
      parsed_url=urlparse(url)
      domain=parsed_url.netloc
      print('domain name',domain)
      response=requests.get(link+'/'+domain)
      response.raise_for_status()
    # access JSOn content
      jsonResponse = response.json()
#print(jsonResponse)
      print('domain name is',jsonResponse['domain'])
      print('ip address is',jsonResponse['ip_address'])
      print('Malware Contents:',jsonResponse['malware'])
      print('Phishing Attack:',jsonResponse['phishing'])
      print('Age of Domain',jsonResponse['domain_age'])
      print('Category Of Website:',jsonResponse['category'])
      domain=jsonResponse['domain']
      ipaddress=jsonResponse['ip_address']
      malware=jsonResponse['malware']
      phishing=jsonResponse['phishing']
      age=jsonResponse['domain_age']
      category=jsonResponse['category']
      rank=jsonResponse['domain_rank']
      score=jsonResponse['risk_score']
      status="safe"
      if malware==True:
          malware="yes"
          status="not safe"
      else:
          malware="no"
          
      if phishing==True:
          phishing="yes"
          status="not safe"
      else:
          phishing="no"
      if malware==True or phishing==True:
               data=scam.objects.filter(domain=domain)
               if data:
                    print('already exists')
               else:
                    category="scam"
                    scammodel(url=url,category=category,status=status).save()
                    notifications.objects.all().delete()
                    notifications(data=url).save()


      return render(request,'listdata.html',{'domain':url,'ip':status,'phishing':phishing,'age':age,'category':category,'rank':rank,'score':score,'malware':malware,phishing:'phishing'})


      #scam(urls=url).save()
      #return render(request,'register.html')
    else:
      dat=notifications.objects.get(id=1) 
      d=dat.data
      return render(request,'index.html',{'data':d})    

def register(request):
    if request.method =='POST':
       fname = request.POST.get('sfname')
       mail1 = request.POST.get('smail')
       passw = request.POST.get('spass')
       reg(fullname=fname,mail=mail1,password=passw).save()
       return render(request,'home.html')
    else:
       return render(request,'register.html')

def login(request):
    if request.method=='POST':
        fname = request.POST.get('sfname')
        passw = request.POST.get('rpass')
        cr = reg.objects.filter(fullname=fname,password=passw)
        if cr:
            return render(request,'home.html',{'user':fname})
        else:
         return render(request,'login.html',{'message':'Invalid Details'})
    else:
       return render(request,'login.html')
    
def url_list(request):
        data=scammodel.objects.all() 
        return render(request,'url_list.html',{'DATA':data})

def result(request):
     return render(request,'result.html')    

def gpt(request):
     if request.method=='POST':
          url=request.POST.get('url')
          response=requests.get(link+'/'+url)
          response.raise_for_status()
    # access JSOn content
          jsonResponse = response.json()
#print(jsonResponse)
          print('domain name is',jsonResponse['domain'])
          print('ip address is',jsonResponse['ip_address'])
          print('Malware Contents:',jsonResponse['malware'])
          print('Phishing Attack:',jsonResponse['phishing'])
          print('Age of Domain',jsonResponse['domain_age'])
          print('Category Of Website:',jsonResponse['category'])
          domain=jsonResponse['domain']
          ipaddress=jsonResponse['ip_address']
          malware=jsonResponse['malware']
          

          phishing=jsonResponse['phishing']
          age=jsonResponse['domain_age']
          category=jsonResponse['category']
          rank=jsonResponse['domain_rank']
          score=jsonResponse['risk_score']
          status="safe"
          if malware==True:
               malware="yes"
               status="Not safe"
          else:
               malware="no"
          if phishing==True:
               phishing="yes"
               status="Not safe"
          else:
               phishing="no"
          
          if malware==True or phishing==True:
               data=scam.objects.get(domain=domain)
               if data:
                    print('already exists')
               else:
                    notifications.objects.all().delete()
                    notifications(data=url).save()


                    scam(urls=url,category=category,domain=domain).save()
          return render(request,'gpt.html',{'domain':domain,'ip':status,'phishing':phishing,'age':age,'category':category,'rank':rank,'score':score,'malware':malware,'phishing':phishing})

     else:
          return render(request,'gpt.html')



def seo(request):
     if request.method=='POST':
          url1=request.POST.get('url')
          url = "https://similar-web.p.rapidapi.com/get-analysis"

          querystring = {"domain":url1}

          headers = {
	                    "X-RapidAPI-Key": "8228a841camsh2b4989400084094p16dbd0jsn95bc8590ae4e",
	                    "X-RapidAPI-Host": "similar-web.p.rapidapi.com"
                    }

          response = requests.get(url, headers=headers, params=querystring)

          print(response.json())
          data=response.json()
          sitename=data['SiteName']
          description=data['Description']
          engagements=data['Engagments']
          bouncerate=engagements['BounceRate']
          bouncerate=float(bouncerate)
          if(bouncerate==0):
               bouncerate=random.uniform(0.08,0.99)
          if bouncerate>0.5:
               bouncestatus="Safe"
          else:
               bouncestatus="Less Secure"
          visits=engagements['Visits']
          visits=int(visits)
          timeonsite=engagements['TimeOnSite']
          timeonsite=float(timeonsite)
          if timeonsite<0.5:
               timestatus="Good Response Time"
          else:
               timestatus="Website Takes Unusual Response Time"
          if visits<1000:
               visitstatus="Page Visits is Very Less"
          elif visits<5000:
               visitstatus="Moderate Page Visits"
          else:
               visitstatus="Good Page Visits"
          if(timeonsite==0):
               timeonsite=random.uniform(0.97,0.99)
          print('bouncerate',engagements['BounceRate'])

          print('pagevisits',engagements['Visits'])
          print('pagevisits',engagements['TimeOnSite'])
          return render(request,'resultseo.html',{'sitename':sitename,'description':description,'bouncerate':bouncerate,'visits':visits,'timeonsite':timeonsite,'bouncestatus':bouncestatus,'visitstatus':visitstatus,'timestatus':timestatus})

     else:
          return render(request,'traffic.html')
def feedbackkk(request):
  if request.method =='POST':
       name = request.POST.get('fname')
       mail1 = request.POST.get('fmail')
       phone1 = request.POST.get('fphone')
       message1 = request.POST.get('fmessage')
       feedback(Name=name,Mail=mail1,Phone=phone1,Message=message1).save()
       return render(request,'index.html')
  else:
       return render(request,'index.html')
def home(request):
     return render(request,'home.html')
def rec(request):
     if request.method=='POST':
          url1=request.POST.get('url')
          url = "https://similar-web.p.rapidapi.com/get-analysis"

          querystring = {"domain":url1}

          headers = {
	                    "X-RapidAPI-Key": "8228a841camsh2b4989400084094p16dbd0jsn95bc8590ae4e",
	                    "X-RapidAPI-Host": "similar-web.p.rapidapi.com"
                    }

          response = requests.get(url, headers=headers, params=querystring)

          print(response.json())
          data=response.json()
          sitename=data['SiteName']
          description=data['Description']
          engagements=data['Engagments']
          bouncerate=engagements['BounceRate']
          bouncerate=float(bouncerate)
          if(bouncerate==0):
               bouncerate=random.uniform(0.08,0.99)
          if bouncerate>0.5:
               bouncestatus="Safe"
          else:
               bouncestatus="Less Secure"
          visits=engagements['Visits']
          visits=int(visits)
          timeonsite=engagements['TimeOnSite']
          timeonsite=float(timeonsite)
          if timeonsite<0.5:
               timestatus="Good Response Time"
          else:
               timestatus="Website Takes Unusual Response Time"
          if visits<1000:
               visitstatus="Page Visits is Very Less"
          elif visits<5000:
               visitstatus="Moderate Page Visits"
          else:
               visitstatus="Good Page Visits"
          if(timeonsite==0):
               timeonsite=random.uniform(0.97,0.99)
          print('bouncerate',engagements['BounceRate'])

          print('pagevisits',engagements['Visits'])
          print('pagevisits',engagements['TimeOnSite'])
          response=requests.get(link+'/'+url1)
          response.raise_for_status()
    # access JSOn content
          jsonResponse = response.json()
#print(jsonResponse)
          print('domain name is',jsonResponse['domain'])
          print('ip address is',jsonResponse['ip_address'])
          print('Malware Contents:',jsonResponse['malware'])
          print('Phishing Attack:',jsonResponse['phishing'])
          print('Age of Domain',jsonResponse['domain_age'])
          print('Category Of Website:',jsonResponse['category'])
          domain=jsonResponse['domain']
          ipaddress=jsonResponse['ip_address']
          malware=jsonResponse['malware']
          phishing=jsonResponse['phishing']
          age=jsonResponse['domain_age']
          category=jsonResponse['category']
          rank=jsonResponse['domain_rank']
          if rank>10000:
               rankstatus="The Websites Rank is above 10000 and have very few regular visits"
          elif rank<5000:
               rankstatus="The website is having good domain rank"
          if phishing==True:
               phishstatus="The website is suspected to fall under phishing category"
          else:
               phishstatus="The website seems to be free from phishing"
          if malware==True:
               malstatus="The website seems to have malicious scripts inside"
          else:
               malstatus="The website is malware free and trusted"
          score=jsonResponse['risk_score']
          return render(request,'recomendations.html',{'sitename':sitename,'description':description,'bouncestatus':bouncestatus,'visitstatus':visitstatus,'timestatus':timestatus,'rankstatus':rankstatus,'phishstatus':phishstatus,'malstatus':malstatus})

     else:
          return render(request,'rec.html')