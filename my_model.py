import requests
from BeautifulSoup import BeautifulSoup

def get_html(URL):
	responce = requests.get(URL)
	return responce.content

def parse_html(content):
	soup = BeautifulSoup(content)
	view_div = soup.find('div', {'class':'view'})
	return view_div.findAll('li')

def find_content(job):
	jj = job.find('div', {'class':'container'})
	title = jj.find('div', {'class': 'title'}).text
	link = jj.find('div', {'class': 'title'}).find('meta', attrs={'itemprop':'url'}).get('content').strip('http://www.gumtree.co.za/a-')
	info = jj.find('div', {'class': 'info'}).find('div', {'class': 'meta-info'}).text
	try:
		job_type = jj.find('ul', {'class': 'attributes'}).findAll('li')[1].text
	except:
		job_type = 'Full-Time'

	return {'title': title.encode('utf-8'), 'info':info.encode('utf-8'), 'link': link, 'job_type': job_type}


def job(jobs):
	jj = []
	for job in jobs:
		if str(job.get('class'))[:6] == 'result':
			jj.append(find_content(job))

	return jj

def page_jobs(page=1):
	URL = 'http://www.gumtree.co.za/s-computing-it-jobs/page-'+str(page)+'/v1c9050p'+str(page)
	html = get_html(URL)
	jobs = parse_html(html)

	return job(jobs)

def get_job_desc(link):
	link = 'http://www.gumtree.co.za/a-'+link
	html = get_html(link)
	soup = BeautifulSoup(html)
	desc = soup.find('div', {'class':'description'})

	return desc.text
