import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from User import User
from profile import ProfilePage
from Modelclass import TwiiterDB
from EditProfile import EditProfile
import os

JINJA_ENVIORMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'

        user = users.get_current_user()

        query = TwiiterDB.query()
        ListOfUsers = list(query.fetch())

        print 'ListOfUSers'
        print ListOfUsers
        print ListOfUsers[0]
        print ListOfUsers[0].username

        template_values = {
        }
        template = JINJA_ENVIORMENT.get_template('search.html')
        self.response.write(template.render(template_values))


    def post(self):

        usernameSearch = self.request.get('username')
        self.response.headers['content-Type'] = 'text/html'





        if self.request.get('button') == 'search':
            checkmg = 'user'
            user = users.get_current_user()

            query = TwiiterDB.query(TwiiterDB.username == usernameSearch)


            ListOfUsers = list(query.fetch())
            print 'listofusers=='
            print ListOfUsers
            print '--'
            print ListOfUsers[0]
            print ListOfUsers[0].username
            template_values = {
                'usernameSearch': usernameSearch,
                'ListOfUsers': ListOfUsers[0].username,
                'checkmg': checkmg
            }
            template = JINJA_ENVIORMENT.get_template('search.html')
            self.response.write(template.render(template_values))






        tempList = []
        if self.request.get('button') == 'searchTweet':
            checkmg = 'tweet'
            queryTweet = TwiiterDB.query()
            ListOfTweet = list(queryTweet.fetch())
            tweetSearch = self.request.get('tweet')

            for tweet in ListOfTweet:


                if len(tweet.tweet) != 0:

                    for eachtweet in tweet.tweet:

                        if tweetSearch in eachtweet:
                            print eachtweet
                            tempList.append(eachtweet)

            template_values = {
                'usernameSearch': usernameSearch,
                'templist': tempList,
                'checkmg': checkmg
            }
            template = JINJA_ENVIORMENT.get_template('search.html')
            self.response.write(template.render(template_values))
















