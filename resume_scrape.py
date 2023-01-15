import requests
from bs4 import BeautifulSoup

DEBUG=input("DEBUG?")
if DEBUG=="no":
    skills = input('Enter your Skill: ').strip().split()
    titles = input('Enter your Title:').strip().split()
    schools = input('Enter your School:').strip().split()
    places = input('Enter the location: ').strip().split()
else:
    skills=["coding"]
    titles=["software", "developer"]
    schools=[]
    places=["india"]

url="https://www.postjobfree.com/resumes?q="
for skill in skills:
    url+=str(skill)+'+'
for title in titles:
    url+=str(title)+'+'
for school in schools:
    url+=str(school)+'+'
url=url[:-1]+'&l='
if len(places)>0:
    for place in places:
        url+=str(place)+'%2C+'
    url=url[:-3]
url+="&radius=100"

response=requests.get(url)

html=response.text
soup=BeautifulSoup(html, "html.parser")

resume_headers=soup.find_all("div", class_="snippetPadding")
for resume_snippets in resume_headers:
    resume_title=resume_snippets.find("h3", class_="itemTitle")
    resume_link=resume_title.find("a")
    print(resume_link.text)
    
    #print(resume_title)
#print(resume_headers)
#print(soup.prettify())
#a=soup.prettify()
#f=open("C:/Users/aarya/Downloads/resume_output.txt", "w")
#f.write(a)
#f.close()

#https://www.postjobfree.com/resumes?q=coding+software+developer+python+java&l=Mumbai%2C+Maharashtra%2C+India&radius=25
