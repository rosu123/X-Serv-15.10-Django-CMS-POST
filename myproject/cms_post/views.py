from django.shortcuts import render
from cms_post.models import Pages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context

# Create your views here.

def mylogout(request):
    logout(request)
    return redirect(barra)

def get_absolute_url(self):

    if not (self.startswith("http://") or self.startswith("https://")):
        self = "http://" + self
    return self


def form_normal():
    resp = "<html><body><h1>DB info:</h1>"
    resp += "<form action='/'' method='post'>"
    resp += "Site:<br> <input type='text' name = 'site' value='Google' required><br>"
    resp += "URL:<br> <input type='text' name = 'url' value='www.google.es' required><br>"
    resp += "<input type='submit' value='Submit'></form></body>"
    return(resp)

def form_template():
    resp = "<html><body><h1>DB info:</h1>"
    resp += "<form action='/annotated/'' method='post'>"
    resp += "Site:<br> <input type='text' name = 'site' value='Google' required><br>"
    resp += "URL:<br> <input type='text' name = 'url' value='www.google.es' required><br>"
    resp += "<input type='submit' value='Submit'></form></body>"
    return(resp)

def edit_content(request, identificador):
    if request.method == "GET":
        #MyModel.objects.filter(pk=some_value).update(field1='some value')
        #o
        #obj = Product.objects.get(pk=pk)
        #obj.name = "some_new_value"
        #obj.save()
        if request.user.is_authenticated():
            resp = ("Logged in as " + request.user.username +
                     ". <a href='/logout/'>Logout</a><br/><br/>")
        else:
            resp = "Not logged in. <a href='/login/'>Login</a><br/><br/>"
        resp += "<a href='/annotated/'>Annotated</a><br/><br/>"
        resp += form_normal()
        try:
            list_urls = Pages.objects.all()
            resp += "<p>Saved URLs:</p>"
            resp += "<ol>"
            #print(resp)
            for pag in list_urls:
                resp += '<li><a href="' + str(pag.id) + '">' + pag.name + "  (" + pag.page + ')</a></li>'
            resp += "</ol>"
            return HttpResponse(resp)
        except OperationalError:
            return HttpResponse("No content", status=404)

    if request.method == "POST" or request.method == "PUT":
        if request.user.is_authenticated():
            name = request.POST['site']
            page = request.POST['url']
            #print("NAME: |" + name + "|    URL: |" + url + "|")
            url = get_absolute_url(page)
            try:
                pag = Pages.objects.get(page = url)
                resp = "It already exist: "
            except ObjectDoesNotExist:
                pag = Pages(name = name, page = url)
                #pag.name = newUrl
                #pag.page = url
                pag.save()
                resp = "URL: "
            resp += "<a href=" + pag.page + ">" + pag.page + "</a>"
            resp += "</br>Shortened: <a href=" + str(pag.id) + ">" + str(pag.id) + "</a> "
            resp += "</br><a href=/>Back</a> "
        else:
            resp = "You cannot modify the DB if you are not logged: "
            resp += '<a href="/login">Login</a>'
        return HttpResponse(resp)


def content(request, identificador):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)
    try:
        pag = Pages.objects.get(id = int(identificador))
        print(pag.page)
        return HttpResponse(pag.page)
    except ObjectDoesNotExist:
        return HttpResponse("Content not found", status=404)


@csrf_exempt
def barra(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            resp = ("Logged in as " + request.user.username +
                     ". <a href='/logout/'>Logout</a><br/><br/>")
        else:
            resp = "Not logged in. <a href='/login/'>Login</a><br/><br/>"
        resp += "<a href='/annotated/'>Annotated</a><br/><br/>"
        resp += form_normal()
        try:
            list_urls = Pages.objects.all()
            resp += "<p>Saved URLs:</p>"
            resp += "<ol>"
            #print(resp)
            for pag in list_urls:
                resp += '<li><a href="' + str(pag.id) + '">' + pag.name + "  (" + pag.page + ')</a></li>'
            resp += "</ol>"
            return HttpResponse(resp)
        except OperationalError:
            return HttpResponse("No content", status=404)

    if request.method == "POST" or request.method == "PUT":
        if request.user.is_authenticated():
            name = request.POST['site']
            page = request.POST['url']
            #print("NAME: |" + name + "|    URL: |" + url + "|")
            url = get_absolute_url(page)
            try:
                pag = Pages.objects.get(page = url)
                resp = "It already exist: "
            except ObjectDoesNotExist:
                pag = Pages(name = name, page = url)
                #pag.name = newUrl
                #pag.page = url
                pag.save()
                resp = "URL: "
            resp += "<a href=" + pag.page + ">" + pag.page + "</a>"
            resp += "</br>Shortened: <a href=" + str(pag.id) + ">" + str(pag.id) + "</a> "
            resp += "</br><a href=/>Back</a> "
        else:
            resp = "You cannot modify the DB if you are not logged: "
            resp += '<a href="/login">Login</a>'
        return HttpResponse(resp)


def contentAnnotated(request, identificador):
    if request.user.is_authenticated():
        login = ("Logged in as " + request.user.username +
                 ". <a href='/logout/'>Logout</a><br/><br/>")
    else:
        login = "Not logged in. <a href='/login/'>Login</a><br/><br/>"

    template = get_template("annotated.html")
    if request.method != "GET":
        content = "Method not allowed"
        resp = Context({'title': login, 'content': content})
        return HttpResponse(template.render(resp), status=405)
    try:
        pag = Pages.objects.get(id = int(identificador))
        print(pag.page)
        content = pag.page
        resp = Context({'title': login, 'content': content})
        return HttpResponse(template.render(resp))
    except ObjectDoesNotExist:
        content = "Content not found"
        resp = Context({'title': login, 'content': content})
        return HttpResponse(template.render(resp), status=404)

@csrf_exempt
def barraAnnotated(request):
    if request.user.is_authenticated():
        login = ("Logged in as " + request.user.username +
                 ". <a href='/logout/'>Logout</a><br/><br/>")
    else:
        login = "Not logged in. <a href='/login/'>Login</a><br/><br/>"
    if request.method == "GET":

        content = "<a href='/'>Normal</a><br/><br/>"
        content += form_template()
        try:
            content += "<p>Saved URLs:</p><ol>"
            list_urls = Pages.objects.all()
            for pag in list_urls:
                content += '<li><a href="' + str(pag.id) + '">' + pag.name + "</a> --> " + pag.page + "</li>"
            content += "</ol>"

            template = get_template("annotated.html")
            resp = Context({'title': login, 'content': content})

            return HttpResponse(template.render(resp))
        except OperationalError:
            content = "<br>No content<br/>"
            template = get_template("annotated.html")
            resp = Context({'title': login, 'content': content})
            return HttpResponse(template.render(resp), status=404)

    if request.method == "POST" or request.method == "PUT":
        if request.user.is_authenticated():
            name = request.POST['site']
            page = request.POST['url']
            #print("NAME: |" + name + "|    URL: |" + url + "|")
            url = get_absolute_url(page)
            try:
                pag = Pages.objects.get(page = url)
                content = "It already exist: "
            except ObjectDoesNotExist:
                pag = Pages(name = name, page = url)
                #pag.name = newUrl
                #pag.page = url
                pag.save()
                content = "URL: "
            content += "<a href=" + pag.page + ">" + pag.page + "</a>"
            content += "</br>Shortened: <a href=/annotated/" + str(pag.id) + ">" + str(pag.id) + "</a> "
            content += "</br><a href=/annotated/>Back</a> "
        else:
            content = "You cannot modify the DB if you are not logged: "
            content += '<a href="/login">Login</a>'
        template = get_template("annotated.html")
        resp = Context({'title': login, 'content': content})

        return HttpResponse(template.render(resp))



def msg_error(request, msg):
    return HttpResponse(msg + ": content not found", status=404)

def show_content(request):
    if request.user.is_authenticated():
        logged = 'Logged in as ' + request.user.username
    else:
        logged = 'Not logged in.'

# Create your views here.
