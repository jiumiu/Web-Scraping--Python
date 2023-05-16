from bs4 import BeautifulSoup
import requests

def extract_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  if request.status_code == 200:
    results = []
    soup = BeautifulSoup(request.text, "html.parser")
    jobs = soup.find_all('table', id="jobsboard")
    for job in jobs:
      job_posts = job.find_all('td', class_="company position company_and_position")
      job_posts.pop(0)
      for post in job_posts:
        anchors = post.find_all('a')
        anchor = anchors[0]
        link = anchor['href']
        company = post.find('h3')
        position = anchor.find('h2')
        locations = post.find_all('div', class_="location")
        salary = "None"
        region = "None"
        type = "None"
        for location_list in locations:
          if location_list.string.startswith('💰') == True:
            salary = location_list.string.strip()
          elif location_list.string.startswith('💰') == False and location_list.string.startswith('⏰') == False:
            region = location_list.string.strip()
          elif location_list.string.startswith('⏰') == True:
            type = location_list.string.strip()
            
        job_data = {
          'Company': company.string.strip(),
          'Position': position.string.strip(),
          'Region': region,
          'Salary': salary,
          'Type': type,
          'Link': f"https://remoteok.com{link}"
        }
        results.append(job_data)

    for result in results:
      print(result)
      print("")
  else: 
    print("Can't get jobs.")

extract_jobs("react")