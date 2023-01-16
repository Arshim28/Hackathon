import requests
from bs4 import BeautifulSoup
import openai
import re


def get_job_keywords(jd):
    
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        
        What is the job title?""".format(jd=jd[:50]),
        temperature=0.7
    )
    format_responses=response.choices[0].text.split()[:3]
    job_titles=[]
    for word in format_responses:
        if len(word)>3 and "-" not in word:
            job_titles.append(word)

    
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        
        What is the country of the job?""".format(jd=jd[:200]),
        temperature=0.3
    )
    format_responses=response.choices[0].text.split()[:2]
    job_locations=[]
    for word in format_responses:
        if len(word)>3 and "-" not in word:
            job_locations.append(word)

    
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        
        What are the skills required for the job?""".format(jd=jd[:2000]),
        temperature=0.3
    )
    format_responses=response.choices[0].text.split()[:3]
    job_skills=[]
    for word in format_responses:
        if len(word)>3 and "-" not in word:
            job_skills.append(word)
    
    
    return job_titles, job_locations, job_skills, []




def get_profiles_postjobfree(skills, titles, schools, places):

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
    url+="&radius=50"

    response=requests.get(url)

    html=response.text
    soup=BeautifulSoup(html, "html.parser")

    resume_headers=soup.find_all("div", class_="snippetPadding")

    job_titles=[]
    job_locations=[]
    job_dates=[]
    names=[]
    emails=[]
    job_skills=[]
    yoes=[]
    
    counter=0
    for resume_snippets in resume_headers:
        
        counter+=1
        if counter==6:
            break
        
        resume_title=resume_snippets.find("h3", class_="itemTitle")
        resume_link="https://www.postjobfree.com"+str(resume_title.find("a")["href"])

        cur_response=requests.get(resume_link)
        cur_html=cur_response.text
        cur_soup=BeautifulSoup(cur_html, "html.parser")

        cur_job_title=cur_soup.find_all("h1")[1].text
        cur_job_location=cur_soup.find("a", class_="colorLocation").text
        cur_job_date=cur_soup.find("span", class_="colorDate").text

        cur_normal_text=cur_soup.find("div", class_="normalText")
        cur_lines=cur_normal_text.find_all("p")
        cur_name=cur_lines[0].text

        cur_email="No email found"
        for cur_line in cur_lines[:5]:
            if "@" in cur_line.text:
                cur_email=cur_line.text
        
        cur_resume=cur_normal_text.text
        openai_response=openai.Completion.create(
            engine="davinci",
            prompt="""
            {resume}
            
            What are the key professional skills?""".format(resume=cur_resume[:1000]),
            temperature=0.3
        )
        cur_skills=str(openai_response.choices[0].text)

        openai_response=openai.Completion.create(
            engine="davinci",
            prompt="""
            {resume}
            
            How many years of experience?""".format(resume=cur_resume[:1000]),
            temperature=0.3
        )
        cur_yoe=str(openai_response.choices[0].text)

        if 'Given' in cur_skills:
            cur_skills="Skills not clearly mentioned"
        
        if 'Given' in cur_yoe:
            cur_yoe="Not found"

        job_titles.append(cur_job_title)
        job_locations.append(cur_job_location)
        job_dates.append(cur_job_date)
        names.append(cur_name)
        emails.append(cur_email)
        job_skills.append(cur_skills)
        yoes.append(cur_yoe)

    return job_titles, job_locations, job_dates, names, emails, job_skills, yoes


def get_profiles_hound(skills, titles, schools, places):

    skill_str=" ".join(skills)+" "+" ".join(titles)
    location_str=" ".join(places)

    print(skill_str, location_str)
    url="https://www.hound.com/employers/resume-search.php"

    parameters={
        "kw": skill_str,
        "locationgen": location_str
    }

    response=requests.post(url, data=parameters)

    html=response.text
    soup=BeautifulSoup(html, "html.parser")

    job_cards=soup.find_all("div", class_="jobTitleWrap")

    job_titles=[]
    job_locations=[]
    job_dates=[]
    job_firms=[]
    education_list=[]
    names=[]
    emails=[]
    job_skills=[]
    yoes=[]

    counter=0
    for card in job_cards:

        counter+=1
        if counter==6:
            break
        
        name=card.find("a", class_="tooltip").text.strip()
        
        paragraph_list=card.find_all("p")
        
        location=paragraph_list[0].text.strip()
        school=paragraph_list[1].text.strip()
        firm=paragraph_list[2].text.strip()
        job_title=paragraph_list[3].text.strip()

        link=card.find("a")["href"]
        cur_url="https://www.hound.com/employers/"+link

        cur_response=requests.get(cur_url)
        cur_html=cur_response.text
        
        cur_soup=BeautifulSoup(cur_html, "html.parser")
        cur_content=cur_soup.find_all("div", class_="content row")

        cur_experience=cur_content[1].text
        cur_education=cur_content[2].text

        cur_skills=cur_soup.find("div", class_="d-flex align-items-center flex-wrap").text.strip()

        theta=1
        while theta<len(cur_skills):
            if ord(cur_skills[theta])<=90 and cur_skills[theta-1]!=" ":
                cur_skills=cur_skills[:theta]+", "+cur_skills[theta:]
                theta+=1
            theta+=1

        job_titles.append(job_title)
        job_locations.append(location)
        job_dates.append("")
        job_firms.append(firm)
        names.append(name)
        emails.append("Email not available")
        job_skills.append(cur_skills)
        yoes.append(cur_experience)
        education_list.append(cur_education)

    return job_titles, job_locations, job_dates, job_firms, names, emails, job_skills, yoes, education_list
        

openai.api_key = ''
if __name__=="__main__":

    jd=''


    titles, places, skills, schools = get_job_keywords(jd)

    #print(skills, titles, schools, places)
    
    job_titles, job_locations, job_dates, names, emails, job_skills, yoes = get_profiles_postjobfree(skills , titles, schools, places)

    #for beta in range(len(job_titles)):
     #   print(job_titles[beta])
      #  print(job_locations[beta])
      #  print(names[beta])
      #  print(emails[beta])
      #  print(emails[beta])
      #  print(job_skills[beta])
      #  print(yoes[beta])

    #print(get_profiles_hound(skills, titles, schools, places))
        
