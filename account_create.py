import urllib, urllib2, re
import pygtk, os, time
pygtk.require('2.0')
import gtk
import mechanize

class CaptchaQuestion:
    def set_image(self,widget,data=None):
        self.image.set_from_file("captcha.png")
    def refresh(self,widget,data=None):
        self.session = SteamPoweredSession()
        self.session.set_captcha_img(self.session.captchagid)
        self.set_image(self)
    def submit(self,widget,data=None):
        print self.session.captchagid + ":" + self.entry.get_text()
        self.session.submit_form(self.entry.get_text())
    def submit_and_refresh(self,widget,data=None):
        self.submit(self)
        self.refresh(self)
    def delete_event(self,widget,event,data=None):
        print "Delete event occurred."
        return False
    def destroy(self,widget,data=None):
        gtk.main_quit()
    def __init__(self):
        self.session = SteamPoweredSession()
        self.session.set_captcha_img(self.session.captchagid)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(1)
        self.window.set_resizable(False)
        self.window.set_title("Steam Account Creator")
        self.hpane = gtk.HPaned()
        self.hpane2 = gtk.HPaned()
        self.vpane = gtk.VPaned()
        self.entry = gtk.Entry(max=0)
        self.button = gtk.Button("Hit Me")
        self.button2 = gtk.Button("Try Again")
        self.button.connect("clicked", self.submit_and_refresh, None)
        self.button2.connect("clicked", self.refresh, None)
        self.hpane.add1(self.entry)
        self.hpane.add2(self.button)
        self.hpane2.add1(self.hpane)
        self.hpane2.add2(self.button2)
        self.vpane.add1(self.hpane2)
        self.image = gtk.Image()
        self.image.set_from_file("captcha.png")
        self.image.show()
        self.vpane.show()
        self.vpane.add2(self.image)
        self.window.add(self.vpane)
        self.hpane.show()
        self.hpane2.show()
        self.button.show()
        self.button2.show()
        self.entry.show()
        self.window.show()
        
    def main(self):
        gtk.main()
class SteamPoweredSession:
    def __init__(self):
        self.url = "https://store.steampowered.com/join/"
        self.site_data = urllib2.urlopen(self.url)
        self.forms = mechanize.ParseResponse(self.site_data, backwards_compat=False)
        self.form = self.forms[1] #currently true, but this line will cause this script to eventually break
        self.captchagid = self.form.find_control(id="captchagid").value
    def submit_form(self, captcha_text):
        email = emails.pop().rstrip()
        password = ""
        name_of_school = ""
        name_prefix = ""
        data = urllib.urlencode({"accountname" : name_prefix + get_next_idler(), "password" : password, "email" : email, "challenge_question" : "NameOfSchool", "secret_answer" : name_of_school, "captchagid" : self.captchagid, "captcha_text" : captcha_text, "i_agree" : "1", "ticket" : "", "count" : "4"})
        f = urllib.urlopen("https://store.steampowered.com/join/createaccount/", data)
        s = f.read()
        print s
        print "============================================="
        if(s == "{\"bSuccess\":true}"):
            inc_idler_num()
            resave_email_list(emails)
        else:
            emails.append(email)
    def set_captcha_img(self, captchagid):
        image = urllib.urlopen("https://store.steampowered.com/public/captcha.php?gid="+captchagid).read()
        f = open("captcha.png", "wb")
        f.write(image)
        f.close()
        
def get_email_list():
    f = open("emails.txt", 'r')
    emails = []
    for line in f:
        line = line.rstrip()
        emails.append(line)
    f.close()
    return emails
def resave_email_list(emails):
    f = open("gmails.txt", 'w')
    email_concatenation = ''
    for gmail in emails:
        email_concatenation += (gmail+'\n')
    email_concatenation = email_concatenation.rstrip()
    f.write(email_concatenation)
def get_next_idler():
    f = open("emailcount.txt", 'r')
    num = f.readline()
    f.close()
    return num
def inc_idler_num():
    num = int(get_next_idler())+1
    f = open("emailcount.txt", 'w')
    f.write(str(num))
    f.close()
if __name__ == "__main__":
    emails = get_email_list()
    captcha_answer = ''
    captcha_window = CaptchaQuestion()
    captcha_window.main()