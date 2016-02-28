from robobrowser import RoboBrowser
import re
import time
import sys

AMAZON_LOGIN_URL = "http://kindle.amazon.com/login"
HIGHLIGHTS_FOR_BOOK_URL = "https://kindle.amazon.com/your_highlights_and_notes/"

def initialize_browser():
    browser = RoboBrowser(history=True, user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13')
    return browser
    
def do_login(browser, email, password):

    browser.open(AMAZON_LOGIN_URL)
    form = browser.get_form(attrs={'name':'signIn'})
    form['email'].value = email
    form['password'].value = password
    browser.submit_form(form)
    return browser

def get_list_of_books_for_page(page):
	return

def get_highlights_for_book_with_id(book_id):
	print ("about to follow link for " + HIGHLIGHTS_FOR_BOOK_URL + book_id)
	#browser.open(HIGHLIGHTS_FOR_BOOK_URL + book_id)
	browser.open("http://localhost:8000/arse.html")
	#print (browser.parsed)
	
	no_highlights_check = browser.find('h1', text='No Highlights')
	if no_highlights_check is not None:
		print ("No highlights for " + book_id)
		return
	else:
		#get the containing div
		data = browser.find('div',attrs={'id':'your_highlightsWrapper'})
		highlights = data.find_all('div', class_=["highlightRow", "bookMain"])
		book_counter = 0
		for highlight in highlights:
			if highlight.has_key('class'):
				if highlight['class'][0] == "bookMain":
					book_counter = book_counter + 1
					if book_counter > 1:
						break
				if highlight['class'][0] == "highlightRow":
					t = highlight.find('span', class_="highlight")
					print (t.text + "\n\n")
			else:
				print ("div without class")
			#if we get more than one book, return
		
username = sys.argv[1]
password = sys.argv[2]

browser  = initialize_browser()
get_highlights_for_book_with_id("123")
#browser = do_login(browser, username, password)

#books_link = browser.get_link('Your Books')
#browser.follow_link(books_link)
#browser.open('http://localhost:8000/index.html')
#books = browser.find_all('a', href=re.compile('/work/*'))


#for book in books:
#	id = re.search('^.*/(.*)$', book['href'])
#	time.sleep(3)
#	get_highlights_for_book_with_id(id.group(1))
    
#data = browser.find_all('div',attrs={'class':'yourReadingPaginationWrapper'})

#pagination_links = data[0].find_all('a', text=re.compile('\d'))

#for a in pagination_links:
#	print (a['href'])


