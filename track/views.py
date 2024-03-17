from django.shortcuts import render,redirect
import pyrebase
from django.http import HttpResponse
import datetime
#firebase config
config = {
  "apiKey": "AIzaSyDw5iS6Lt6XhHQutJrSVvi8eLe1gk8CmYM",
  "authDomain": "bugtracking-58802.firebaseapp.com",
  "databaseURL": "https://bugtracking-58802-default-rtdb.firebaseio.com",
  "projectId": "bugtracking-58802",
  "storageBucket": "bugtracking-58802.appspot.com",
  "messagingSenderId": "528636520411",
  "appId": "1:528636520411:web:518ca1a7f93c799f8669fe"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
# Create your views here.
def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        cat=request.POST.get('cat')
        data = {
            'name':username,
            'password':pwd,
            'category':cat
            }
        db.child("users").push(data)
        return redirect("/login")
    return render(request, "signup.html")
def home(request):
    bugs=db.child("userbugs").get().val()
    return render(request, "home.html",{'bugs':bugs})
def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        cat=request.POST.get('cat')
        print(username,pwd,cat)
        users = db.child("users").get()
        for user in users.each():
            a=user.val()
            if a['category'] == cat and a['password'] == pwd and a['name'] ==username:
                if cat == 'user':
                    return redirect("/usersform")
                elif cat =='projectmanager':
                    return redirect("/home")
                else:
                    return redirect("/signup")
            else:
                print('no')
    return render(request,"login.html")
def usersform(request):
    time = datetime.datetime.now()
    time = time.strftime("%d-%m-%Y")
    if request.method =='POST':
        url=request.POST.get('url')
        un=request.POST.get('un')
        pwd=request.POST.get('pwd')
        desc=request.POST.get('desc')
        print(url,un,pwd,desc)
        is_pm=True
        is_tester=False
        is_cleared=False
        time=time
        data = {
            'url':url,
            'username':un,
            'password':pwd,
            'desc':desc,
            'is_pm':is_pm,
            'is_tester':is_tester,
            'is_cleared':is_cleared,
            'time':time
        }
        db.child("userbugs").push(data)
        return redirect('/usersform')
    return render(request,'usersform.html')
def testerview(request):
    bugs=db.child("userbugs").get().val()
    filtered_data = {key: value for key, value in bugs.items() if value.get('username', "raja")}
    print("hi",filtered_data)
    return render(request,'testerview.html',{'filtered_data': filtered_data})