from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import requests
# Create your views here.

def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None):#如果is_login为真
        print("request.session",request.session.get('is_login'))
        return redirect('/index/')#重定向到index

    if request.method=="POST":
        login_form=forms.UserForm(request.POST)#使用request.post方法提取出请求数据 在传给form.UserForm付给login_form
        message="请检查填写的内容"
        if login_form.is_valid():#如果login_form为真
            username=login_form.cleaned_data.get('username')#取出username password
            password=login_form.cleaned_data.get('password')
            print("PASSWORD1",password)

            try:
                user = models.User.objects.get(name=username)
            except:
                message = "用户不存在"
                return render(request,'login/login.html',locals())

            print("PASSWORD2", password)

            if user.password == password:
                print("password3",password)
                request.session['is_login']=True
                request.session['user_id']=user.id
                request.session['user_name']=user.name
                return redirect('/index/')

            else:
                message="密码不正确"
                return render(request,'login/login.html',locals())
            print("password4",password)
        else:
            return render(request,"login/login.html",locals())
    login_form=forms.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')

    if request.method=='POST':
        register_form=forms.RegisterForm(request.POST)
        print("register_form>>>>",register_form)
        message="请检查填写内容"
        if register_form.is_valid():
            username=register_form.cleaned_data.get('username')
            password1=register_form.cleaned_data.get('password1')
            password2=register_form.cleaned_data.get('password2')
            email=register_form.cleaned_data.get('email')
            sex=register_form.cleaned_data.get('sex')

            if password1!=password2:
                message="两次输入密码不同"
                return render(request,'login/register.html',locals())
            else:
                same_name_user=models.User.objects.filter(name=username)
                if same_name_user:
                    message='用户名已经存在'
                    return render(request,'login/register.html',locals())

                same_name_user=models.User.objects.filter(email=email)
                if same_name_user:
                    message="该邮箱已经注册"
                    return render(request,'login/register.html',locals())

                new_user=models.User()
                new_user.name=username
                new_user.password=password1
                new_user.email=email
                new_user.sex=sex
                new_user.save()

                return redirect('/login/')
        else:
             return render(request,'login/register.html',locals())
    register_form=forms.RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')

