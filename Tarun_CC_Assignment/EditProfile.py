import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from User import User
from profile import ProfilePage
from Modelclass import TwiiterDB
import os

JINJA_ENVIORMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class EditProfile(webapp2.RequestHandler):
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

        userNameSave = self.request.get('edit')
        print userNameSave

        # PutTwitter.following = userNameSave
        GetTwitter = ndb.Key(TwiiterDB, user.user_id())

        UserInfo = GetTwitter.get()
        template_values = {
            'login_logouturl': login_logouturl,
            'login_logout': login_logout,
            'user': user,
            'UserInfo': UserInfo,
            'edit': 'edit'
        }
        template = JINJA_ENVIORMENT.get_template('EditProfile.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()

        GetTwitter = ndb.Key(TwiiterDB, user.user_id())
        print 'user---'
        username = GetTwitter.get().username

        PutTwitter = TwiiterDB(id=user.user_id())

        PutTwitter.username = username
        PutTwitter.collegework = self.request.get('collegework')
        PutTwitter.Firstname = self.request.get('Firstname')
        PutTwitter.Lastname = self.request.get('lastname')
        #PutTwitter.Email = user.email()
        print '===='
        print  PutTwitter.Firstname
        PutTwitter.put()

