import openai
import re

openai.api_key="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"


def get_job_title(jd):
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        What is that job title?""".format(jd=jd),
        temperature=0.3
    )
    format_responses=response.choices[0].text.split()

    words=[]
    for word in format_responses:
        if len(word)>3 and re.match('^[a-zA-Z0-9]*$', word):
            words.append(word)
    
    return format_responses


def get_job_location(jd):
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        What is the country of that job?""".format(jd=jd),
        temperature=0.3
    )
    format_responses=response.choices[0].text.split()

    words=[]
    for word in format_responses:
        if len(word)>3 and re.match('^[a-zA-Z0-9]*$', word):
            words.append(word)
    
    return format_responses


def get_job_skills(jd):
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        What is the skill required for the job?""".format(jd=jd),
        temperature=0.7
    )
    format_responses=response.choices[0].text.split()

    words=[]
    for word in format_responses:
        if len(word)>3 and re.match('^[a-zA-Z0-9]*$', word):
            words.append(word)
    
    return format_responses


def get_work_experience(jd):
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        What is the work experience required for the job?""".format(jd=jd),
        temperature=0.3
    )
    format_responses=response.choices[0].text.split()

    words=[]
    for word in format_responses:
        if len(word)>3 and re.match('^[a-zA-Z0-9]*$', word):
            words.append(word)
    
    return words


def get_education(jd):
    response=openai.Completion.create(
        engine="davinci",
        prompt="""
        Job Description: {jd}
        What is the education required for the job?""".format(jd=jd),
        temperature=0.3
    )
    format_responses=response.choices[0].text.split()

    words=[]
    for word in format_responses:
        if len(word)>3 and re.match('^[a-zA-Z0-9]*$', word):
            words.append(word)
    
    return format_responses

jd="""
Role: Software Engineer II – Google
Minimum qualifications:
• Bachelor’s degree or equivalent practical experience.
• 1 year of experience with software development in one or more programming languages
(e.g., Python, C, C++, Java, JavaScript).
• 1 year of experience with data structures or algorithms.
Preferred qualifications:
• Master's degree or PhD in Computer Science or related technical field.
• 1 year of experience building and developing large-scale infrastructure, distributed systems
or networks, and/or experience with compute technologies, storage, and/or hardware
architecture.
• Experience developing accessible technologies.
About The Job:
Google's software engineers develop the next-generation technologies that change how billions of
users connect, explore, and interact with information and one another. Our products need to handle
information at massive scale, and extend well beyond web search. We're looking for engineers who
bring fresh ideas from all areas, including information retrieval, distributed computing, large-scale
system design, networking and data storage, security, artificial intelligence, natural language
processing, UI design and mobile; the list goes on and is growing every day. As a software engineer,
you will work on a specific project critical to Google’s needs with opportunities to switch teams and
projects as you and our fast-paced business grow and evolve. We need our engineers to be versatile,
display leadership qualities and be enthusiastic to take on new problems across the full-stack as we
continue to push technology forward.
With your technical expertise you will manage project priorities, deadlines, and deliverables. You will
design, develop, test, deploy, maintain, and enhance software solutions.
Google Cloud accelerates organizations’ ability to digitally transform their business with the best
infrastructure, platform, industry solutions and expertise. We deliver enterprise-grade solutions that
leverage Google’s cutting-edge technology – all on the cleanest cloud in the industry. Customers in
more than 200 countries and territories turn to Google Cloud as their trusted partner to enable
growth and solve their most critical business problems.
Responsibilities:
• Write product or system development code.
• Participate in, or lead design reviews with peers and stakeholders to decide amongst
available technologies.
• Review code developed by other developers and provide feedback to ensure best practices
(e.g., style guidelines, checking code in, accuracy, testability, and efficiency).
• Contribute to existing documentation or educational content and adapt content based on
product/program updates and user feedback.
• Triage product or system issues and debug/track/resolve by analyzing the sources of issues
and the impact on hardware, network, or service operations and quality.
Google is proud to be an equal opportunity workplace and is an affirmative action employer. We are
committed to equal employment opportunity regardless of race, color, ancestry, religion, sex,
national origin, sexual orientation, age, citizenship, marital status, disability, gender identity or
Veteran status. We also consider qualified applicants regardless of criminal histories, consistent with
legal requirements. See also Google's EEO Policy and EEO is the Law. If you have a disability or special
need that requires accommodation, please let us know by completing our Accommodations for
Applicants form.
"""


print(get_job_title(jd))
print(get_job_location(jd))
print(get_job_skills(jd))
print(get_work_experience(jd))
print(get_education(jd))






