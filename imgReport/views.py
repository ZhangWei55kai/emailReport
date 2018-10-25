# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.db import connections
import re,json
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.views import View
from forms import UserLoginInfo,UserRegisterForm,PermisForm
from django.views.generic.base import TemplateView
from imgReport.models import User,Permis
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from collections import OrderedDict

# Create your views here.

class userLogin(View):
    @method_decorator(login_required(login_url='/getLoginPage/', redirect_field_name='next'))
    def get(self,request):
        print request.user.username
        return JsonResponse({'1':'2'})

    def post(self,request):
        userForm = UserLoginInfo(request.POST)
        print userForm
        if userForm.is_valid():
            username = userForm.cleaned_data['userName']
            password = userForm.cleaned_data['passWord']
            print password,username
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'code':'200','result':'login success'})
            else:
                return JsonResponse({'code':'0','result':'login failed'})
        else:
            return JsonResponse({'code':'-1','result':userForm.errors})



class getLoginPage(TemplateView):

    template_name = "./AdminLTE-master/pages/examples/login.html"


    def get_context_data(self, **kwargs):
        context = super(getLoginPage, self).get_context_data()
        pass

class getRegisterPage(TemplateView):
    template_name = "./AdminLTE-master/pages/examples/register.html"
    def post(self,request):
        print request.POST
        userForm = UserRegisterForm(request.POST)
        print userForm
        if userForm.is_valid():
            userName = userForm.cleaned_data.get('userName',None)
            passWord = userForm.cleaned_data.get('passWord',None)
            email = userForm.cleaned_data.get('email',None)
            userModel = User.objects.create_user(username=userName,
                                     password=passWord,
                                     email=email)
            return JsonResponse({'code':'200','result':'注册成功'})
        else:
            return JsonResponse({'code':'0','result':userForm.errors})


class getIndexPage(TemplateView):
    template_name = "./AdminLTE-master/index.html"


    def dispatch(self, request, *args, **kwargs):
        result = super(getIndexPage,self).dispatch( request, *args, **kwargs)
        return result

    @method_decorator(login_required(login_url='/getLoginPage/', redirect_field_name='next'))
    def get(self,request):
        template_name = "./AdminLTE-master/index.html"
        return render(request,template_name)

class Logout(View):


    @method_decorator(login_required(login_url='/getLoginPage/', redirect_field_name='next'))
    def get(self,request):
        try:
            logout(request)
            return JsonResponse({'code':200,'result':'注销成功'})
        except Exception as e:
            return JsonResponse({'code':0,'result':'注销失败'})


class getPermissionPage(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        result = super(getPermissionPage, self).dispatch(request, *args, **kwargs)
        return result

    @method_decorator(login_required(login_url='/getLoginPage/', redirect_field_name='next'))
    def get(self, request):
        template_name = "./user.html"
        return render(request, template_name)


class createPermission(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        result = super(createPermission, self).dispatch(request, *args, **kwargs)
        return result

    @method_decorator(login_required(login_url='/getLoginPage/', redirect_field_name='next'))
    def get(self, request):
        template_name = "./permissionPage.html"
        return render(request, template_name)

    @method_decorator(login_required(login_url='/getLoginPage/', redirect_field_name='next'))
    def post(self,request):
        perForm = PermisForm(request.POST)
        if perForm.is_valid():
            name = perForm.cleaned_data.get('name',None)
            url = perForm.cleaned_data.get('url',None)
            try:
                perModel = Permis(name=name,
                                  url=url)
                perModel.save()
                perM = Permis.objects.all().order_by('id').first()
                result = {'newName':perM.name,'newUrl':perM.url,'newId':perM.id}
            except Exception as e:
                print e
                return JsonResponse({'code':'-1','result':'未知错误'})
            return JsonResponse({'code':'200','result':'创建成功','data':result})
        else:
            return JsonResponse({'code':'0','result':'创建失败'})


@login_required(login_url='/getLoginPage/', redirect_field_name='next')
def getUserinfo(request):
    userModel = User.objects.all()
    userList=[]
    for i in userModel:
        dataDict = {}
        dataDict['id'] = i.id
        dataDict['username'] = i.username
        dataDict['last_login'] = str(i.last_login)
        dataDict['email'] = i.email
        userList.append(dataDict)
    jsonData = json.dumps(userList)
    return HttpResponse(jsonData,content_type="application/json")


def getPermisionList(request):
    perModel = Permis.objects.all()
    perList = []
    for i in perModel:
        dataDict = {}
        dataDict['id'] = i.id
        dataDict['name'] = i.name
        dataDict['url'] = i.url
        perList.append(dataDict)
    jsonData = json.dumps(perList)
    return HttpResponse(jsonData,content_type='application/json')


def getCur():
        cursor = connections['test'].cursor()
        return cursor


def getTestCur():
    cursor = connections['default'].cursor()
    return cursor

def getSql(verId):
    newBugSql =  '''SELECT count(*) FROM 
                    (SELECT * FROM nodeassociation WHERE ASSOCIATION_TYPE = 'IssueVersion'
                     AND SOURCE_NODE_ENTITY = 'Issue' ) a
                    INNER JOIN projectversion b ON a.SINK_NODE_ID=b.id 
                    INNER JOIN jiraissue c ON a.SOURCE_NODE_ID = c.id WHERE
                     a.SINK_NODE_ID = %s AND c.issuetype=1'''%verId
    fixBugSql = newBugSql + ''' AND c.issuestatus = 6'''
    return [newBugSql,fixBugSql]

def getChildSql(verIds,flag):
    sql = []
    if flag == 'allBug':
        for ver in verIds:
            bug = '''SELECT count(*) FROM 
                    (SELECT * FROM nodeassociation WHERE ASSOCIATION_TYPE = 'IssueVersion'
                     AND SOURCE_NODE_ENTITY = 'Issue' ) a
                    INNER JOIN projectversion b ON a.SINK_NODE_ID=b.id 
                    INNER JOIN jiraissue c ON a.SOURCE_NODE_ID = c.id WHERE
                     a.SINK_NODE_ID = %s AND c.issuetype=1'''%ver
            sql.append(bug)
        return sql
    if flag == 'everyClose':
        for ver in verIds:
            closeBug = '''SELECT count(*) FROM 
                    (SELECT * FROM jiraissue) ji
                    INNER JOIN customfieldvalue cv ON ji.id = cv.ISSUE
                    INNER JOIN projectversion pv ON pv.id = NUMBERVALUE
                    WHERE cv.CUSTOMFIELD = 10729 AND NUMBERVALUE = %s '''%ver
            sql.append(closeBug)
        return sql


def getVersion(data,x):
    d = []
    c = []
    for i in range(len(data)):
        li = re.findall(r'(\w*[0-9]+)\w*', data[i][1])
        if len(li) == 4:
        # if len(li) == 2:
            c.append(data[i])
        else:
            d.append(data[i])

    if x == 'son':
        strId = [str(j[0]) for j in c]
        verDict = zip(strId, [j[1] for j in c])
        return verDict
    else:
        strId = [str(j[0]) for j in d]
        verDict = zip(strId, [j[1] for j in d])
        return verDict


def getDataBySql(data):
    VERDICT = []
    for i in range(len(data)):
        verDict = {}
        verDict['key'] = str(data[i][0])
        verDict['value'] = str(data[i][1])
        VERDICT.append(verDict)

    return VERDICT


#--------------------测试报告界面
@login_required(login_url='/getLoginPage/', redirect_field_name='next')
def index(requests):
    if requests.method == 'GET':
        cursor = getCur()
        cursor.execute('select id,pname from project')
        result = cursor.fetchall()
        projectModel = dict(result)
    return render(requests,"TestReport.html",{'context':projectModel})

#-------------------获取所有项目版本号接口

def getProjectVer(requests,proId):
    if requests.method == 'GET':
       cursor = getCur()
       cursor.execute('SELECT id FROM `jiraissue`WHERE issuetype IN (10200,10300) AND project='+proId)
       result = cursor.fetchall()
       idResult = ','.join([str(i[0]) for i in result])
       if idResult:
           SQLStr = '''SELECT id,vname FROM `projectversion` WHERE id IN (
           SELECT NUMBERVALUE FROM `customfieldvalue` WHERE CUSTOMFIELD =
           10304 AND issue IN(%s))'''%idResult
           cursor.execute(SQLStr)
           verResult =cursor.fetchall()
           verDict = getVersion(verResult,'fuqin')
       else:
           verDict = {}
       return JsonResponse({'version':dict(verDict)})


#---------------查询是否为子版本或父版本
def isSonVerOrParVer(requests,proId,Vname):
    if requests.method == 'GET':
        cursor = getCur()
        SQLStr = '''SELECT id,vname FROM `projectversion` WHERE
                    project = {0} AND
                    (UPPER(vname) LIKE '{1}%' OR 
                    LOWER(vname) LIKE '{1}%') '''.format(proId,Vname)
        cursor.execute(SQLStr)
        verAll = cursor.fetchall()
        print verAll
        if len(verAll)>1:
            result = {}
            verDict = dict(getVersion(verAll,'son'))
            result['flag']=True
            result['childVer'] = verDict
            return JsonResponse(result)
        else:
            return JsonResponse({'result':False})







	
#---------------查询该版本下的所有bug
def getAllBug(requests,verId):
    if requests.method == 'GET':
        cursor = getCur()
        sql = getSql(verId)
        cursor.execute(sql[0])
        newBug = cursor.fetchall()
        cursor.execute(sql[1])
        fixBug = cursor.fetchall()
        dataSheet = {'newBug':newBug[0],'fixBug':fixBug[0]}
        return JsonResponse(dataSheet)






'''
数据第一个版本5个，第二个版本5个,第一版本解决3个，第二版本解决7个

总bug数         ：逐步递增的bug数比如，那么第一版本5，第二版本10 SqlFlag = allBug
每版新增bug数    ：如上  第一版本5个，第二版本5个  SqlFlag = everyCreate
每版关闭bug数    ：如上  第一版本3个，第二版本7个（为了区分是在哪个版本解决的加上issueFixVersion）SqlFlag = everyClose 
总未关闭bug数    ：如上  第一版本2个，第二版本0个 
'''

#----------------查询子版本下所有bug
def getChildVerBug(requests):
    if requests.method == 'POST':
        ids = requests.POST.get('data')
        idlist =  eval(ids)['ids']
        verName = eval(ids)['verName']
        idDict = eval(ids)['idAllList']
        #总bug数
        allBugNum = []
        #每版新增bug数
        everyCreateNum = []
        #每版关闭bug数
        everyCloseNum = []
        #每版未关闭bug数
        allUnCloseNum = []
        cur = getCur()
        sqlListCreate = getChildSql(idlist,'allBug')
        try:
            for S in sqlListCreate:
                cur.execute(S)
                everyCreateNum.append(cur.fetchall()[0][0])
            print everyCreateNum
        except Exception as e:
            everyCreateNum = []
            print e
        if everyCreateNum:
            _num = 0
            for i in everyCreateNum:
                _num+=i
                allBugNum.append(_num)
        sqlListClose = getChildSql(idlist,'everyClose')
        try:
            for S in sqlListClose:
                cur.execute(S)
                everyCloseNum.append(cur.fetchall()[0][0])
        except Exception as e:
            everyCloseNum = []
            print e
        try:
            for length in range(len(allBugNum)):
                if length == 0:
                    result = everyCreateNum[length]-everyCloseNum[length]
                    allUnCloseNum.append(result)
                else:
                    result = allUnCloseNum[length-1]+(everyCreateNum[length]-everyCloseNum[length])
                    allUnCloseNum.append(result)
        except Exception as e:
            allUnCloseNum = []

        sheetData = {'allBugNum':allBugNum,
                     'everyCreateNum':everyCreateNum,
                     'everyCloseNum':everyCloseNum,
                     'allUnCloseNum':allUnCloseNum,
                     'verName':verName}

        return JsonResponse(sheetData)

@login_required(login_url='/getLoginPage/', redirect_field_name='next')
def sendEmailByContext(requests):
    if requests.method == 'GET':
        return render(requests,'email.html')

    if requests.method == 'POST':
        emailData = requests.POST
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = emailData['emailTitle']
        text_content = emailData['htmlContext']
        sendTo = emailData['reciveMem'].split(',')
        ccTo = emailData['CCMem'].split(',')
        try:
            if sendTo != None or sendTo != '':
                msg = EmailMultiAlternatives(subject=subject,
                                             body=text_content,
                                             from_email=from_email,
                                             to=sendTo,
                                             bcc=ccTo,)
                msg.attach_alternative(text_content, 'text/html')
                msg.send()
                return JsonResponse({'result': '邮件发送成功'})
            else:
                return JsonResponse({'result': '收件人不能为空'})
        except Exception as e:
            print e
            return JsonResponse({'result': '邮件发送功能异常'})


def getEmailInfo(requests):
    if requests.method == 'GET':
        cur = getTestCur()
        cur.execute('SELECT id,createdata FROM mail_content ORDER BY id DESC ')
        html = cur.fetchall()
        cur.execute('select content from mail_content order by id DESC limit 1')
        content = cur.fetchall()
        result = getDataBySql(html)
        result.append({'content':content[0][0]})
        JsonResult = json.dumps(result)
        return  HttpResponse(JsonResult,content_type="application/json")
    if requests.method == 'POST':
        id = requests.POST.get('id',None)
        if id != None:
            cur = getTestCur()
            sql = 'select content from mail_content where id=%s'%id
            print sql
            cur.execute(sql)
            content = cur.fetchall()[0][0]
            return JsonResponse({'content': content})
        else:

            return JsonResponse({'message':'error'})


def saveEmail(requests):
    if requests.method == 'POST':
        EmailData = requests.POST
        text = EmailData.get('text',None)
        id = EmailData.get('id',None)
        cur = getTestCur()
        sql = "update mail_content set content='%s' where id=%s"%(text,id)
        print sql
        try:
            cur.execute(sql)
        except Exception as e:
            return JsonResponse({'result':'数据异常，修改失败'})
        return JsonResponse({'result':'修改成功'})
