from django.shortcuts import render
from . import resume_scrape
from bs4 import BeautifulSoup
import requests

def results(request):
    if request.method == "POST":
        query = request.POST.get('search')
        if query == "":
            return render(request, 'home.html')
        else:
            resume_scrape.jd = query
            skills, titles, schools, places = resume_scrape.get_job_keywords(resume_scrape.jd)
            #print(skills, titles, schools, places)
            job_titles, job_locations, job_dates, names, emails, job_skills, yoes = resume_scrape.get_profiles_postjobfree(skills,
                                                                                                             titles,
                                                                                                             schools,
                                                                                                             places)
            results = []

            for beta in range(len(job_titles)):
                results.append((job_titles[beta],job_locations[beta], names[beta], emails[beta], job_skills[beta], yoes[beta]))

            job_titles, job_locations, job_dates, job_firms, names, emails, job_skills, yoes, education_list = resume_scrape.get_profiles_hound(skills,
                                                                                                             titles,
                                                                                                             schools,
                                                                                                             places)

            for beta in range(len(job_titles)):
                results.append((job_titles[beta], job_locations[beta], job_dates[beta], job_firms[beta], names[beta], emails[beta], job_skills[beta], yoes[beta], education_list[beta]))

            context = {
                'results':results
            }
            return render(request, 'results.html', context)
    else:
        return render(request, 'results.html')

def about(request):
    return render(request, 'about.html')

def query(request):
    return render(request, 'home.html')