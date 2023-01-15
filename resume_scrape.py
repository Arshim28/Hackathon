import requests
from bs4 import BeautifulSoup


DEBUG = input("DEBUG?")
if DEBUG == "no":
    skills = input('Enter your Skill: ').strip().split()
    titles = input('Enter your Title:').strip().split()
    schools = input('Enter your School:').strip().split()
    places = input('Enter the location: ').strip().split()
else:
    skills = ["coding"]
    titles = ["software", "developer"]
    schools = []
    places = ["india"]

url = "https://www.postjobfree.com/resumes?q="
for skill in skills:
    url += str(skill)+'+'
for title in titles:
    url += str(title)+'+'
for school in schools:
    url += str(school)+'+'
url = url[:-1]+'&l='
if len(places) > 0:
    for place in places:
        url += str(place)+'%2C+'
    url = url[:-3]
url += "&radius=100"

# Resumes = []
url += f"&p=1"
for i in range(2, 10):
    url = url[:-1] + f"{i}"
    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    resume_headers = soup.find_all("div", class_="snippetPadding")

    for resume_snippets in resume_headers:
        resume_title = resume_snippets.find("h3", class_="itemTitle")
        resume_link = resume_title.find("a")
        print("Job Title" + resume_link.text)
        resume_description = resume_snippets.find("div", class_="normalText")
        resume_location = resume_description.find("span")
        print(resume_location.text)
        print("--------------------")
