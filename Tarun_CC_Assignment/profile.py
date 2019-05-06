import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from Modelclass import TwiiterDB
from User import User

import os

JINJA_ENVIORMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ProfilePage(webapp2.RequestHandler):
    def get(self):

        self.response.headers['content-Type'] = 'text/html'
        # self.response.write('hello world')
        login_logouturl = ''
        login_logout = ''
        welcomemsg = 'welcome back'
        myuser = None
        user = users.get_current_user()
        if user:
            login_logouturl = users.create_logout_url(self.request.uri)
            login_logout = 'logout'
            myuser_key = ndb.Key('User', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcomemsg = 'Welcome to the application'
                myuser = User(id=user.user_id())
                myuser.put()

        else:
            login_logouturl = users.create_login_url(self.request.uri)
            login_logout = 'login'

        # follow sugestion



        #query = TwiiterDB.query()
        #ListOfUsers = list(query.fetch())
        query = TwiiterDB.query(TwiiterDB.Email == user.email())
        ListOfUsers = list(query.fetch())
        print 'profile user==='
        print ListOfUsers


        PutTwitter = TwiiterDB(id=user.user_id())
        userNameSave = self.request.get('follow_Name')

        print 'usernameSave'
        print userNameSave


        if userNameSave:
            listOfusersOfzero = ListOfUsers[0]

            GetTwitter = ndb.Key(TwiiterDB, user.user_id())
            listingTweet = GetTwitter.get().tweet
            print 'listing of twitter--'
            print listingTweet


            template_values = {
                'login_logouturl': login_logouturl,
                'login_logout': login_logout,
                'username': userNameSave,
                'welcome': welcomemsg,
                'ListOfUsers': ListOfUsers,
                'tweetlisting': listingTweet
            }
            template = JINJA_ENVIORMENT.get_template('showProfile.html')
            self.response.write(template.render(template_values))

        else:

            #print ListOfUsers[0]
            #print ListOfUsers[0].Email

            if len(userNameSave) > 1:
                print 'inside---'
                #PutTwitter.following = userNameSave
                GetTwitter = ndb.Key(TwiiterDB, user.user_id())

                PutTwitter.username = GetTwitter.get().username
                PutTwitter.tweet = GetTwitter.get().tweet
                PutTwitter.following = userNameSave
                PutTwitter.put()


            if len(ListOfUsers) != 0:

                listOfusersOfzero = ListOfUsers[0]
                print "list---"
                print user.email()
                print ListOfUsers[0].Email

                template_values = {
                    'login_logouturl': login_logouturl,
                    'login_logout': login_logout,
                    'user': user,
                    'welcome': welcomemsg,
                    'edit': "edit",
                    'ListOfUsers': ListOfUsers,
                    'ListofusersZero': listOfusersOfzero
                }
                template = JINJA_ENVIORMENT.get_template('profile.html')
                self.response.write(template.render(template_values))

            else:
                template_values = {
                    'login_logouturl': login_logouturl,
                    'login_logout': login_logout,
                    'user': user,
                    'welcome': welcomemsg,
                    'edit': "edit",
                    'ListOfUsers': ListOfUsers,

                }
                template = JINJA_ENVIORMENT.get_template('profile.html')
                self.response.write(template.render(template_values))




    def post(self):

        self.response.headers['Content - Type'] = 'text / html'
        user = users.get_current_user()
        myuser = None

        if user:
            login_logouturl = users.create_logout_url(self.request.uri)
            login_logout = 'logout'
            myuser_key = ndb.Key('User', user.user_id())
            myuser = myuser_key.get()
            print "myuser--"
            print myuser
            if myuser == None:
                welcomemsg = 'Welcome to the application'
                myuser = User(id=user.user_id())
                myuser.put()

        else:
            login_logouturl = users.create_login_url(self.request.uri)
            login_logout = 'login'
            print "error case"
        print "user--"
        print

        PutTwitter = TwiiterDB(id=user.user_id())
        # GetTwitter

        GetTwitter = ndb.Key(TwiiterDB, user.user_id())

        PutTwitter.username = GetTwitter.get().username
        PutTwitter.Email = GetTwitter.get().Email
        PutTwitter.Firstname = GetTwitter.get().Firstname
        PutTwitter.Lastname = GetTwitter.get().Lastname
        PutTwitter.collegework = GetTwitter.get().collegework

        tweet = self.request.get('tweet')
        listOfTwitter = GetTwitter.get().tweet

        listOfTwitter.append(tweet)
        PutTwitter.tweet = listOfTwitter
        PutTwitter.put()
