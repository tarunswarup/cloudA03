import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from User import User
from profile import ProfilePage
from search import Search
from showProfile import Show
from Modelclass import TwiiterDB
from EditProfile import EditProfile
import os

JINJA_ENVIORMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'
        # self.response.write('hello world')
        login_logouturl = ''
        login_logout = ''
        welcomemsg = 'welcome back'
        myuser = None
        user = users.get_current_user()
        if user:
            print 'user'
            login_logouturl = users.create_logout_url(self.request.uri)
            login_logout = 'logout'
            myuser_key = ndb.Key(User, user.user_id())
            myuser = myuser_key.get()



            if myuser == None:
                welcomemsg = 'Welcome to the application'
                myuser = User(id=user.user_id())
                myuser.put()
                print "my user keyname-----"




            if myuser.username == None:
                print 'usernam.html'
                query = User.query()
                ListOfUsers = list(query.fetch())
                login_logouturl = users.create_login_url(self.request.uri)

                template_values = {
                    'login_logouturl': login_logouturl,
                    'login_logout': login_logout,
                    'user': user,
                    'welcome': welcomemsg,
                    'myuser': myuser,
                    'ListOfUsers': ListOfUsers
                }
                template = JINJA_ENVIORMENT.get_template('username.html')
                self.response.write(template.render(template_values))
            else:
                print 'main'
                print 'else middle'
                login_logouturl = users.create_login_url(self.request.uri)
                login_logout = 'logout'
                query = TwiiterDB.query()
                ListOfUsers = list(query.fetch())
                template_values = {
                    'login_logouturl': login_logouturl,
                    'login_logout': login_logout,
                    'user': user,
                    'welcome': welcomemsg,
                    'myuser': myuser,
                    'ListOfUsers': ListOfUsers
                }
                template = JINJA_ENVIORMENT.get_template('Home.html')
                self.response.write(template.render(template_values))

        else:
            print 'user else'
            login_logouturl = users.create_login_url(self.request.uri)
            login_logout = 'login'
            query = TwiiterDB.query()
            ListOfUsers = list(query.fetch())
            template_values = {
                'login_logouturl': login_logouturl,
                'login_logout': login_logout,
                'user': user,
                'welcome': welcomemsg,
                'myuser': myuser,
                'ListOfUsers': ListOfUsers
            }
            template = JINJA_ENVIORMENT.get_template('Home.html')
            self.response.write(template.render(template_values))











        # if len(ListOfUsers) != 0:
        #     print 'list of users main---'
        #     print ListOfUsers
        #     print ListOfUsers[0]
        #     print ListOfUsers[0].tweet
        #
        #
        #     if ListOfUsers[0].username == None:
        #         template_values = {
        #         'login_logouturl': login_logouturl,
        #         'login_logout': login_logout,
        #         'user': user,
        #         'welcome': welcomemsg,
        #         'myuser': myuser
        #         }
        #         template = JINJA_ENVIORMENT.get_template('Username.html')
        #         self.response.write(template.render(template_values))
        #     else:
        #
        #         template_values = {
        #             'login_logouturl': login_logouturl,
        #             'login_logout': login_logout,
        #             'user': user,
        #             'welcome': welcomemsg,
        #             'myuser': myuser,
        #             'ListOfUsers': ListOfUsers
        #              }
        #         template = JINJA_ENVIORMENT.get_template('Home.html')
        #         self.response.write(template.render(template_values))
        # else:
        #
        #     template_values = {
        #         'login_logouturl': login_logouturl,
        #         'login_logout': login_logout,
        #         'user': user,
        #         'welcome': welcomemsg,
        #         'myuser': myuser,
        #         'ListOfUsers': ListOfUsers
        #     }
        #     template = JINJA_ENVIORMENT.get_template('username.html')
        #     self.response.write(template.render(template_values))


    def post(self):
        user = users.get_current_user()
        print 'user---'
        print user
        GetTwitter = TwiiterDB(id=user.user_id())

        GetTwitter.username = self.request.get('username')
        GetTwitter.collegework = self.request.get('college/work')
        GetTwitter.Firstname = self.request.get('firstname')
        GetTwitter.Lastname = self.request.get('lastname')
        #GetTwitter.tweet = ['None']
        GetTwitter.Email = user.email()
        print '===='
        print  GetTwitter.Firstname
        GetTwitter.put()
        myuser = User(id=user.user_id())
        myuser.username = self.request.get('username')
        myuser.put()


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfilePage),
    ('/EditProfile',EditProfile),
    ('/search',Search),
    ('/showProfile',Show)

], debug=True)
