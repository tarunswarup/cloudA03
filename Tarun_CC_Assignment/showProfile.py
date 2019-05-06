import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from User import User
from profile import ProfilePage
from search import Search
from Modelclass import TwiiterDB
from EditProfile import EditProfile
import os

JINJA_ENVIORMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Show(webapp2.RequestHandler):
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

        userName = self.request.get('user')
        print userName

        query = TwiiterDB.query(TwiiterDB.username == userName)
        profileList = list(query.fetch())

        print 'profileList checking---'
        print profileList


        template_values = {
            'login_logouturl': login_logouturl,
            'login_logout': login_logout,
            'user': user,
            'welcome': welcomemsg,
            'userName': userName,
            'profileList': profileList
        }
        template = JINJA_ENVIORMENT.get_template('showProfile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content - Type'] = 'text / html'
        user = users.get_current_user()
        userName = self.request.get('username')
        print 'follow--'
        print userName
        GetTwitter = ndb.Key(TwiiterDB, user.user_id())
        PutTwitter = TwiiterDB(id=user.user_id())

        if self.request.get('button') == 'follow':
            print 'foloww-=uygf'
            #query = TwiiterDB.query(TwiiterDB.username == userName)
            #profileList = list(query.fetch())
            listFollowing = GetTwitter.get().following
            PutTwitter.username = GetTwitter.get().username
            PutTwitter.Email = GetTwitter.get().Email
            PutTwitter.Firstname = GetTwitter.get().Firstname
            PutTwitter.Lastname = GetTwitter.get().Lastname
            PutTwitter.collegework = GetTwitter.get().collegework
            PutTwitter.tweet = GetTwitter.get().tweet
            listFollowing.append(userName)
            PutTwitter.following = listFollowing
            PutTwitter.put()

