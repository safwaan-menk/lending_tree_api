from bs4 import BeautifulSoup
import requests
import lxml
import json

# get the status of the target request
url = 'https://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc/45102840/?sort=&pid='

def setup(url):
    try:
        response = requests.get(url)
        return BeautifulSoup(response.text, 'lxml')
    except:
        return 0

def extractsoup(soup):
    reviewData = {}
    #get lender details
    
    lenderInformation = soup.find('div', class_ = 'lenderHeader')
    try:
        reviewData['lenderName'] = lenderInformation.find('h1').text
    except:
        return 0
    reviewData['lenderRating'] = lenderInformation.find('p', class_='total-reviews').text.split(' ', 1)[0]
    lenderRecommendedContainer = lenderInformation.find('div', class_='recommend-text')
    reviewData['lenderRecommendedPercentage'] = lenderRecommendedContainer.find('span').text.replace('%', '')

    #review information and breakdown
    reviewSummary = {}
    reviewRatings = soup.find('div', class_ = 'start-rating-reviews')
    reviewSummary['totalReviews'] = reviewRatings.find('b', class_ = 'hidden-xs').text
    reviewBreakdown = soup.find('div', class_ = 'reviews-breakdown')
    starBreakdown = reviewBreakdown.find_all('a')
    currentMaxRating=5
    for starRatings in starBreakdown:
        stars = 'star' if currentMaxRating == 1 else 'stars' 
        reviewSummary[f'{currentMaxRating}{stars} : '] = starRatings.text.replace('(', '').replace(')', '')
        currentMaxRating-=1
    reviewData['reviewSummary'] = reviewSummary


    # get the review container
    reviewInformation = []
    reviewList = soup.find_all('div', class_ =['col-xs-12 mainReviews', 'col-xs-12 mainReviews hiddenReviews'])

    for reviews in reviewList:
        reviewProperties = {}
        #get a review's star rating
        reviewProperties['reviewStarRating'] = list(reviews.find('div', class_ = 'numRec').text)[1]
        reviewProperties['lenderRecommended'] = reviews.find('div', class_ = 'lenderRec').text if reviews.find('div', class_ = 'lenderRec') else 'Not Recommended'
        
        #get a reviews details
        reviewDetails = reviews.find_all('div', class_ = 'reviewDetail')
        #get review points
        reviewPoints = reviews.find_all('div', class_ = 'reviewPoints')

        for review in reviewDetails:
            #extract title, text, author, and date from review
            reviewProperties['reviewTitle'] = review.find('p', class_ = 'reviewTitle').text.strip()
            reviewProperties['reviewText'] = review.find('p', class_ = 'reviewText').text.strip()
            reviewProperties['reviewAuthor'] = ' '.join(review.find('p', class_ = 'consumerName').text.split())
            reviewProperties['reviewDate'] = review.find('p', class_ = 'consumerReviewDate').text.strip()

        for reviewPoint in reviewPoints:
            reviewProperties['closedWithLender'] = reviewPoint.find('div', class_ = 'yes').text if reviewPoint.find('div', class_ = 'yes') else "No"
            loanDetails = reviewPoint.find_all('div', class_ = 'loanType')
            for loan in loanDetails:
                reviewProperties['loan'] = loan.text
        reviewInformation.append(reviewProperties)

    reviewData["reviewInformation"] = reviewInformation
    
    return reviewData if len(reviewData["reviewInformation"]) !=0 else 0


# Not working
# def getlastpage(soup):
#     print(soup)
#     page = soup.find('ul', class_='lenderNav pagination')
#     print(page)
#     page.find_all('li', class_='page-link')['aria-label']
#     if(page[-1] != 'Next Page'):
#         url = 'https://www.lendingtree.com/reviews/mortgage/ratekingcom-a-div-of-riverside-mortgage-professionals-corp/36709604/?sort=&pid='+ page[-1].split(' ', 1) [1]
#         return url
#     else:
#         return


