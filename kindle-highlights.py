from robobrowser import RoboBrowser
import re
import time
import sys

AMAZON_LOGIN_URL = "http://kindle.amazon.com/login"
HIGHLIGHTS_FOR_BOOK_URL = "https://kindle.amazon.com/your_highlights_and_notes/"
USER_AGENT = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"

def initialize_browser():

    browser = RoboBrowser(history=True, user_agent=USER_AGENT)
    return browser
    
def do_login(browser, email, password):

    browser.open(AMAZON_LOGIN_URL)
    form = browser.get_form(attrs={'name':'signIn'})
    form['email'].value = email
    form['password'].value = password
    browser.submit_form(form)
    return browser

def get_highlights_for_book_with_id(book_id):

	browser.open(HIGHLIGHTS_FOR_BOOK_URL + book_id)	
	
	no_highlights_check = browser.find('h1', text='No Highlights')
	if no_highlights_check is not None:
		return
	else:
		highlights = browser.find_all('div', class_=["highlightRow", "bookMain"])
		book_counter = 0
		for highlight in highlights:				
			if highlight['class'][0] == "bookMain":
				book_counter = book_counter + 1
				# check we've not loaded up another book
				if book_counter > 1:
					break					
				title = highlight.find('span', class_='title')
				author = highlight.find('span', class_='author')
			if highlight['class'][0] == "highlightRow":
				# text is in a span
				t = highlight.find('span', class_="highlight")
				print (title.text + " " + author.text + " " + t.text + "\n")

def get_highlights_for_books_on_page(books_link):

	browser.follow_link(books_link)
	books = browser.find_all('a', href=re.compile('/work/*'))

	for book in books:
		# the last part of the URL is the book id
		id = re.search('^.*/(.*)$', book['href'])
		get_highlights_for_book_with_id(id.group(1))

#
# execution starts here
#		
username = sys.argv[1]
password = sys.argv[2]

browser  = initialize_browser()
browser = do_login(browser, username, password)

first_page_of_books_link = browser.get_link('Your Books')
browser.follow_link(first_page_of_books_link)

# first grab the pagination links - we'll need them in a minute
pagination_data = browser.find_all('div',attrs={'class':'yourReadingPaginationWrapper'})
pagination_links = pagination_data[0].find_all('a', text=re.compile('\d'))

# get books from the first page
get_highlights_for_books_on_page(first_page_of_books_link)

# then go through the pagination links
for pagination_link in pagination_links:
	get_highlights_for_books_on_page(pagination_link)