from django.shortcuts import render

from bs4 import BeautifulSoup
import requests

def results(request):
    if request.method == "POST":
        query = request.POST.get('search')
        if query == "":
            return render(request, 'home.html')
        else:

            results = []
            page = requests.get('https://search17.lycos.com/web/?q='+query).text
            soup = BeautifulSoup(page,'lxml')
            listings = soup.find_all(class_="result-item")
            for content in listings:
                title = content.find(class_='result-title').text
                description = content.find(class_='result-description').text
                link = content.find(class_='result-link').text
                url = content.find(class_='result-url').text
                results.append((title,description,url))
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