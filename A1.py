import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import MyUser
from data import data
from reve import reve

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type'] = 'text/html'
            url = ''
            url_string = ''
            myuser=''
            user =''
            welcome = 'Welcome back'
            user= users.get_current_user()
            y=''
            if user:
                y=reve.query().fetch()
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'
                template = JINJA_ENVIRONMENT.get_template('option.html')
                self.response.write(template.render())
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()
                if myuser == None:
                    welcome = 'Welcome to the application'
                    myuser = MyUser(id=user.user_id())
                    myuser.email_address=user.email()
                    myuser.put()
            else:
                y=reve.query().fetch()
                url = users.create_login_url(self.request.uri)
                url_string = 'login'
                template = JINJA_ENVIRONMENT.get_template('option.html')
                self.response.write(template.render())

            template_values = {
            'y':y,
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser
        }
            template = JINJA_ENVIRONMENT.get_template('A1.html')
            self.response.write(template.render(template_values))

class Data(webapp2.RequestHandler):
    def get(self):
        user= users.get_current_user()
        if user:
            x=data.query(
            data.name==self.request.get('name'),
            data.manufacturer==self.request.get('manufacturer'),
            data.year==int(self.request.get('year'))
            ).fetch()
            if len(x)==0:
                ab=data(id=self.request.get('name'))
                ab.name=self.request.get('name')
                ab.manufacturer=self.request.get('manufacturer')
                ab.year=int(self.request.get('year'))
                ab.batterysize=int(self.request.get('batterysize'))
                ab.wltprange=int(self.request.get('wltprange'))
                ab.cost=int(self.request.get('cost'))
                ab.power=int(self.request.get('power'))
                ab.put()
                self.response.write("!!!Inserted successfully!!!!")
            else:
                self.response.write("!!!!error!!!")
        else:
            self.response.write("Please login to Add data!!!!!!")
            url = users.create_login_url(self.request.uri)
            url_string = 'login'



class datret(webapp2.RequestHandler):
    def get(self):
        y=''
        y1=data.query()
        y2=''
        b1=data.query()
        b2=''
        w1=data.query()
        w2=''
        c1=data.query()
        c2=''
        p1=data.query()
        p2=''
        action =self.request.get('Search')
        if action =='Search':
            if self.request.get('t1')=='' and self.request.get('t2')=='' and self.request.get('t3')=='' and self.request.get('t3.2')=='' and self.request.get('t4')=='' and self.request.get('t4.2')=='' and self.request.get('t5')=='' and self.request.get('t5.2')=='' and self.request.get('t6')=='' and self.request.get('t6.2')=='' and self.request.get('t7')=='' and self.request.get('t7.2')=='':
                y=data.query().fetch()
            else:
                try:
                    n=list(data.query().filter(data.name==self.request.get('t1')).fetch(keys_only=True))
                except ValueError:
                    pass
                try:
                    m=list(data.query().filter(data.manufacturer==self.request.get('t2')).fetch(keys_only=True))
                except ValueError:
                    pass
                try:
                    y1=y1.filter(data.year>=int(self.request.get('t3')))
                    y2=list(y1.filter(data.year<=int(self.request.get('t3.2'))).fetch(keys_only=True))
                except ValueError:
                    pass
                try:
                    b1=b1.filter(data.batterysize>=int(self.request.get('t4')))
                    b2=list(b1.filter(data.batterysize<=int(self.request.get('t4.2'))).fetch(keys_only=True))
                except ValueError:
                    pass
                try:
                    w1=w1.filter(data.wltprange>=int(self.request.get('t5')))
                    w2=list(w1.filter(data.wltprange<=int(self.request.get('t5.2'))).fetch(keys_only=True))
                except ValueError:
                    pass
                try:
                    c1=c1.filter(data.cost>=int(self.request.get('t6')))
                    c2=list(c1.filter(data.cost<=int(self.request.get('t6.2'))).fetch(keys_only=True))
                except ValueError:
                    pass
                try:
                    p1=p1.filter(data.power>=int(self.request.get('t7')))
                    p2=list(p1.filter(data.power<=int(self.request.get('t7.2'))).fetch(keys_only=True))
                except ValueError:
                    pass
                #Start of loop for Searchs
                #start of name loop
                if len(n)>0:
                    if len(m)>0:
                        #manufacturer
                        if len(y2)>0:
                            #batterysize
                            if len(b2)>0:
                                #wltprange
                                if len(w2)>0:
                                    #cost start
                                    if len(c2)>0:
                                        #for power
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,w2,c2))
                                        #power end
                                        #cost
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,w2))
                                        #cost end
                                    #wltprange
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,b2))
                                #wltprange
                                #batterysize
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,y2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,y2))
                            #batterysize
                            #year
                        else:
                            if len(b2)>0:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,b2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,b2))
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(m,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(m))
                        #Year
                        #manufacturer
                    else:
                        if len(y2)>0:
                            if len(b2)>0:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2))
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2))
                        else:
                            if len(b2)>0:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(y2,b2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(y2,b2))
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(c2,p2))
                                        else:
                                            y=ndb.get_multi(set(n).intersection(c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(n).intersection(p2))
                                        else:
                                            y=ndb.get_multi(n)
                    #manufacturer
                    #name
                else:
                    if len(m)>0:
                        if len(y2)>0:
                            #batterysize
                            if len(b2)>0:
                                #wltprange
                                if len(w2)>0:
                                    #cost start
                                    if len(c2)>0:
                                        #for power
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,w2,c2))
                                        #power end
                                        #cost
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,w2))
                                        #cost end
                                    #wltprange
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,b2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,b2))
                                #wltprange
                                #batterysize
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(y2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(y2))
                            #batterysize
                            #year
                        else:
                            if len(b2)>0:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(b2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(b2))
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(c2,p2))
                                        else:
                                            y=ndb.get_multi(set(m).intersection(c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(m).intersection(p2))
                                        else:
                                            y=ndb.get_multi(m)
                        #Year
                        #manufacturer
                    else:
                        if len(y2)>0:
                            if len(b2)>0:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(b2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(b2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(b2))
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(b2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(c2,p2))
                                        else:
                                            y=ndb.get_multi(set(y2).intersection(c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(y2).intersection(p2))
                                        else:
                                            y=ndb.get_multi(y2)
                        else:
                            if len(b2)>0:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(b2).intersection(y2,w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(b2).intersection(y2,w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(b2).intersection(y2,w2,p2))
                                        else:
                                            y=ndb.get_multi(set(b2).intersection(y2,w2))
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(b2).intersection(y2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(b2).intersection(y2,b2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(b2).intersection(y2,p2))
                                        else:
                                            y=ndb.get_multi(b2)
                            else:
                                if len(w2)>0:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(b2).intersection(w2,c2,p2))
                                        else:
                                            y=ndb.get_multi(set(b2).intersection(w2,c2))
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(b2).intersection(w2,p2))
                                        else:
                                            y=ndb.get_multi(w2)
                                else:
                                    if len(c2)>0:
                                        if len(p2)>0:
                                            y=ndb.get_multi(set(c2).intersection(p2))
                                        else:
                                            y=ndb.get_multi(c2)
                                    else:
                                        if len(p2)>0:
                                            y=ndb.get_multi(p2)
                                        else:
                                            #y=data.query().fetch()
                                            self.response.write("No similar data found!!!!!")
                    #manufacturer
                    #end of name
                    #end of loop for Search
        template_values={
            'y':y,
            'name':self.request.get('name'),
            'manufacturer':self.request.get('manufacturer'),
            'year':self.request.get('year'),
            'batterysize':self.request.get('batterysize'),
            'wltprange':self.request.get('wltprange'),
            'cost':self.request.get('cost'),
            'power':self.request.get('power')
        }
        action = self.request.get('button')
        if action == 'View':
            self.redirect('/editdel')
            template = JINJA_ENVIRONMENT.get_template('eidel.html')
            self.response.write(template.render(template_values))

        template = JINJA_ENVIRONMENT.get_template('datasearch.html')
        self.response.write(template.render(template_values))


class option(webapp2.RequestHandler):
    def get(self):
        action = self.request.get('button')
        user=users.get_current_user()
        if action == 'Add':
            if user:
                template = JINJA_ENVIRONMENT.get_template('dataupload.html')
                self.response.write(template.render())
            else:
                self.response.write("Please login to Add Data to ev!!!!!")
        elif action == 'Search':
                self.redirect('/datret')
        elif action=='Compare':
                self.redirect('/comp')


class editdel(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            y=None
            action=self.request.get('Edit')
            action1=self.request.get('Delete')
            action3=self.request.get('Review')
            template_values={
            'y':y,
            'name':self.request.get('name'),
            'manufacturer':self.request.get('manufacturer'),
            'year':self.request.get('year'),
            'batterysize':self.request.get('batterysize'),
            'wltprange':self.request.get('wltprange'),
            'cost':self.request.get('cost'),
            'power':self.request.get('power'),
            'e1':self.request.get('e1'),
            'e2':self.request.get('e2'),
            'e3':self.request.get('e3')
            }
            if self.request.get('Edit'):
                name=self.request.get('name')
                year=str(self.request.get('year'))
                manufacturer=self.request.get('manufacturer')
                y = data.query(
                data.name==self.request.get('e1'),
                data.manufacturer==self.request.get('e2'),
                data.year==int(self.request.get('e3'))
                ).fetch()
                if len(y)==0:
                    id=name
                    k=ndb.Key('data',id).get()
                    k.key.delete()
                    ab= data(id=self.request.get('e1'))
                    ab.name=self.request.get('e1')
                    ab.manufacturer= self.request.get('e2')
                    ab.year=int(self.request.get('e3'))
                    ab.batterysize=int(self.request.get('e4'))
                    ab.wltprange=int(self.request.get('e5'))
                    ab.cost=int(self.request.get('e6'))
                    ab.power=int(self.request.get('e7'))
                    ab.put()
                    self.response.write("Data successfully Edit")
                else:
                    self.response.write('The data has been already exists.!!!!!!!')

            elif action1 =='Delete':
                    id=self.request.get('e1')
                    k=ndb.Key('data',id).get()
                    k.key.delete()
                    self.response.write("Data Deleted Successfully.")

            elif action3=='Review':
                template = JINJA_ENVIRONMENT.get_template('rewiew.html')
            template = JINJA_ENVIRONMENT.get_template('eidel.html')
            self.response.write(template.render(template_values))
        else:
            self.response.write("Please login to Delete or Edit or give Review!!!!!")


class comp(webapp2.RequestHandler):
    def get(self):
        y=data.query().fetch()
        action= self.request.get('submit')
        c={}
        z=[]
        count=0
        if action=='submit':
            c=self.request.get('check',allow_multiple=True)
            for i in c:
                count=count +1
            if count<2:
                self.response.write('please select at lease 2 data')
            else:
                for i in c:
                    b=ndb.Key(data,i).get()
                    z.append(b)

        template_values={
            'y':y,
            'z':z
        }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))

class rev(webapp2.RequestHandler):
    def get(self):
        name=self.request.get('name')
        user=users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        action=self.request.get('submit')
        name=self.request.get('name')
        if action:
            y=reve.query(reve.limit==self.request.get('name')+""+user.user_id()).fetch()
            if len(y)==0:
                ab=reve()
                ab.limit=self.request.get('name')+""+user.user_id()
                ab.carname=self.request.get('name')
                ab.custrev=self.request.get('custrev')
                ab.rate=self.request.get('rate')
                ab.put()
                self.response.write("review submited!!!!")
            else:
                self.response.write("You have already reviewed!!!!")
        template_values={
            'name':self.request.get('name')
        }
        template = JINJA_ENVIRONMENT.get_template('rewiew.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([ ('/', MainPage),('/option',option),('/Data',Data),('/datret',datret),('/editdel',editdel),('/rev',rev),('/comp',comp)], debug=True)
