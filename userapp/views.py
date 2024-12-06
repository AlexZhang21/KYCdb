from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Prefetch
from django.contrib import messages
from django.conf import settings
from django.forms.models import model_to_dict

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage

from .forms import UserForm, CreateNewUserForm, changePasswordForm, companyForm, filterForm
from .models import CompanyFile, CompanycreatedRecord, Company, comp_type, product, payment, bank
from datetime import datetime

import os, shutil, mimetypes

# 用户登录视图
def loginPage(request):
    if request.method == 'POST':
        usrnme = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=usrnme, password=pwd)
        if user is not None:
            request.session['user'] = {
                'usrname': user.get_username(),
                'fullname': user.get_full_name(),
                'admin': user.is_superuser,
            }
            login(request, user)
            return redirect('/content_table')
        else:
            messages.error(request, 'username OR password incorrect')
    return render(request, 'userapp/index.html')

# 主页视图
def homePage(request):
    fs = FileSystemStorage()
    if request.user.is_anonymous:
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    form = filterForm()
    form.fields['company_type'].choices = comp_type
    form.fields['product'].choices = product
    form.fields['payment'].choices = payment
    form.fields['issuing_bank'].choices = bank
    form.fields['receiving_bank'].choices = bank
    form.fields['tt_bank'].choices = bank
    all_details = Company.objects.all().prefetch_related()
    return render(request, 'userapp/content_table.html', {'form': form, 'company_list': all_details, 'base': 'userapp/base2.html'})

# 创建公司视图，包含文件上传
def create_company_form(request):
    if request.user.is_anonymous:
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    if request.method == 'POST':
        form = companyForm(request.POST, request.FILES)
        if form.is_valid():
            changes = form.save(commit=False)
            companyname = request.POST.get('company_name')
            counter_onboard = request.POST.get('counterparty_onboard_status')
            serenity_onboard = request.POST.get('serenity_onboard_status')
            checkcompany_name = Company.objects.filter(company_name=companyname).values()
            if len(checkcompany_name) > 0:
                messagess = 'Duplicated name in company name!'
                return render(request, 'userapp/create_new_details.html', {'form': form, 'messages': messagess, 'base': 'userapp/base.html'})
            if counter_onboard == 'Complete':
                changes.counterparty_onboard_date = datetime.today()
            if serenity_onboard == 'Complete':
                changes.serenity_onboard_date = datetime.today()
            changes.save()
            form.save_m2m()

            # 获取新上传的公司详情记录
            getimport = Company.objects.filter(company_name=companyname).values()
            if len(getimport) == 0:
                messagess = 'Something wrong with database! No company name here'
                return render(request, 'userapp/create_new_details.html', {'form': form, 'messages': messagess, 'base': 'userapp/base.html'})
            if len(getimport) != 1:
                messagess = 'Duplicated name in company name! Please contact admin!'
                return render(request, 'userapp/create_new_details.html', {'form': form, 'messages': messagess, 'base': 'userapp/base.html'})

            # 保存公司创建记录
            saverecordobj = CompanycreatedRecord()
            saverecordobj.company_id = int(getimport[0]['id'])
            saverecordobj.done_by = request.user.get_full_name()
            saverecordobj.date = datetime.today()
            saverecordobj.remark = companyname + ' created by ' + request.user.get_full_name()
            saverecordobj.save()

            newcmpname = companyname.replace(" ", "_")
            locdir = os.path.join(settings.MEDIA_ROOT, newcmpname)
            # 检查目录是否存在
            if os.path.exists(locdir):
                shutil.rmtree(locdir)
            os.mkdir(locdir)

            if len(request.FILES) > 0:
                for a in request.FILES.getlist('file_upload'):
                    with open(os.path.join(locdir, a.name), 'wb+') as destination:
                        for chunks in a.chunks():
                            destination.write(chunks)
                    saveobj = CompanyFile()
                    saveobj.filename = a.name
                    saveobj.filepath = os.path.join(locdir, a.name)
                    saveobj.company_id = int(getimport[0]['id'])
                    saveobj.uploaded_date = datetime.today()
                    saveobj.save()

                    # 保存文件上传记录
                    saverecordobj = CompanycreatedRecord()
                    saverecordobj.company_id = int(getimport[0]['id'])
                    saverecordobj.done_by = request.user.get_full_name()
                    saverecordobj.date = datetime.today()
                    saverecordobj.remark = request.user.get_full_name() + ' uploaded file ' + a.name
                    saverecordobj.save()

            form = companyForm()
            return redirect('Home')
        else:
            return render(request, 'userapp/create_new_details.html', {'form': form, 'base': 'userapp/base.html'})
    else:
        form = companyForm()
    return render(request, 'userapp/create_new_details.html', {'form': form, 'base': 'userapp/base.html'})

# 其他视图函数...


def companyPage(request,pk):
    if request.user.is_anonymous:
        print('lol not again')
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')

    com_record = CompanycreatedRecord.objects.select_related('company').filter(company_id=pk)
    compan = Company.objects.get(id=pk)
    # print(com_record.values())
    com_name = str(compan.company_name)
    # print(model_to_dict(com_record))
    # print(com_record.company.company_name)
    print('Company page')
    return render(request, 'userapp/company_details.html', {'comp_record': com_record,'com_name':com_name, 'base': 'userapp/base.html'})
def upload_files(request):
    if request.method == 'POST':
        form = companyForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_upload')
        if form.is_valid():
            for file in files:
                # Process each file here (e.g., save to model or filesystem)
                print(file.name)  # Example action
            return JsonResponse({'message': 'Files uploaded successfully!'})
    else:
        form = companyForm()
    return render(request, 'userapp/upload.html', {'form': form})
def userPage(request, pk):
    print('User page')
    if request.user.is_anonymous:
        print('lol not again')
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    if request.user.id != pk and not request.user.is_superuser:
        messages.error(request,'You are not the user!!')
        return redirect('Home')
    try:
        certain_user = User.objects.get(id=pk)
    except:
        messages.error(request,'User not existed!!!')
        return redirect('Home')
    if request.method == 'POST':
        form = UserForm(request.POST, instance=certain_user)
        # print(form)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('Ad_User_details')
            else:
                return redirect('Home')
    else:
        form = UserForm(instance=certain_user)
    return render(request,'userapp/user_details.html', {'form': form, 'base': 'userapp/base.html'})

def edit_Company(request, pk):
    print('Edit company page')
    comp_item = Company.objects.all().prefetch_related().get(id=pk)
    if request.user.is_anonymous:
        print('lol not again')
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    if request.method == 'POST':
        form = companyForm(request.POST, instance=comp_item)
        # print(form)
        if form.is_valid():
            changes = form.save(commit=False)
            # declare here
            check = Company.objects.get(id=pk)

            changes_dict = {}
            for intech in form.changed_data:
                if intech == 'company_type':
                    norm = [new.company_type for new in check.company_type.all()]
                elif intech == 'payment':
                    norm = [new.payment_type for new in check.payment.all()]
                elif intech == 'product':
                    norm = [new.product_type for new in check.product.all()]
                elif intech == 'issuing_bank':
                    norm = [new.bank_name for new in check.issuing_bank.all()]
                elif intech == 'receiving_bank':
                    norm = [new.bank_name for new in check.receiving_bank.all()]
                elif intech == 'tt_bank':
                    norm = [new.bank_name for new in check.tt_bank.all()]
                else:
                    norm = Company.objects.values_list(intech,flat=True).filter(id=pk)
                norm = list(norm)
                norm = [str(new) for new in norm]
                # print(norm)
                norm_str = ','.join(norm)
                if len(norm_str) == 0:
                    norm_str = 'empty'
                # print(norm_str)
                changes_dict[intech] = norm_str
            # print(form.has_changed())
            # print(form.changed_data)

            counter_onboard = request.POST.get('counterparty_onboard_status')
            serenity_onboard = request.POST.get('serenity_onboard_status')
            if counter_onboard == 'Complete':
                if check.counterparty_onboard_status != 'Complete':
                    changes.counterparty_onboard_date = datetime.today()
            if serenity_onboard == 'Complete':
                if check.serenity_onboard_status != 'Complete':
                    changes.serenity_onboard_date = datetime.today()
            changes.save()
            form.save_m2m()

            # refind again
            checkagn = Company.objects.get(id=pk)
            for item in changes_dict.keys():
                if item == 'company_type':
                    norm = [new.company_type for new in checkagn.company_type.all()]
                elif item == 'payment':
                    norm = [new.payment_type for new in checkagn.payment.all()]
                elif item == 'product':
                    norm = [new.product_type for new in checkagn.product.all()]
                elif item == 'issuing_bank':
                    norm = [new.bank_name for new in checkagn.issuing_bank.all()]
                elif item == 'receiving_bank':
                    norm = [new.bank_name for new in checkagn.receiving_bank.all()]
                elif item == 'tt_bank':
                    norm = [new.bank_name for new in checkagn.tt_bank.all()]
                else:
                    norm = Company.objects.values_list(item,flat=True).filter(id=pk)
                norm = list(norm)
                norm = [str(new) for new in norm]
                norm_str = ','.join(norm)
                if len(norm_str) == 0:
                    norm_str = 'empty'

                saverecordobj = CompanycreatedRecord()
                saverecordobj.company_id = pk
                saverecordobj.done_by = request.user.get_full_name()
                saverecordobj.date = datetime.today()
                saverecordobj.remark = request.user.get_full_name() + ' edited '+ item +' record from ' + changes_dict[item] + ' into ' + norm_str
                saverecordobj.save()
            return redirect('Home')
    else:
        form = companyForm(instance=comp_item)
    return render(request,'userapp/edit_company_details.html', {'form': form, 'base': 'userapp/base.html'})

def company_file(request,pk):
    if request.user.is_anonymous:
        print('lol not again')
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    print('Company file page')
    comp_file = CompanyFile.objects.filter(company_id=pk)
    compan = Company.objects.get(id=pk)
    com_name = str(compan.company_name)
    if request.method == 'POST':
        if len(request.FILES) > 0:
            newcmpname = com_name.replace(" ", "_")
            locdir = os.path.join(settings.MEDIA_ROOT, newcmpname)

            if not os.path.exists(locdir):
                # make record
                saverecordobj = CompanycreatedRecord()
                saverecordobj.company_id = pk
                saverecordobj.done_by = request.user.get_full_name()
                saverecordobj.date = datetime.today()
                saverecordobj.remark = 'Directory '+ newcmpname + ' has missing. Rebuild'
                saverecordobj.save()
                os.mkdir(locdir)
            # check if directory exist or not
            for a in request.FILES.getlist('file_upload'):
                print(a.name)
                with open(os.path.join(locdir, a.name), 'wb+') as destination:
                    for chunks in a.chunks():
                        destination.write(chunks)
                saveobj = CompanyFile()
                saveobj.filename = a.name
                saveobj.filepath = os.path.join(locdir, a.name)
                saveobj.company_id = pk
                saveobj.uploaded_date = datetime.today()
                saveobj.save()

                # make record
                saverecordobj = CompanycreatedRecord()
                saverecordobj.company_id = pk
                saverecordobj.done_by = request.user.get_full_name()
                saverecordobj.date = datetime.today()
                saverecordobj.remark = request.user.get_full_name() + ' uploaded file ' + a.name
                saverecordobj.save()
        else:
            messages.error(request, 'Form not valid!!')
        comp_file = CompanyFile.objects.filter(company_id=pk)
        compan = Company.objects.get(id=pk)
        com_name = str(compan.company_name)
    form = companyForm()
    return render(request, 'userapp/company_file.html',
                  {'comp_file': comp_file, 'com_name': com_name,'form':form,'prim':pk, 'base': 'userapp/base.html'})

def delete_file(request,pk):
    print('delete file')
    comp_file = CompanyFile.objects.get(id=pk)
    file_path = str(comp_file.filepath)
    filename = str(comp_file.filename)
    comp_id = int(comp_file.company_id)
    if os.path.exists(file_path):
        # make record
        saverecordobj = CompanycreatedRecord()
        saverecordobj.company_id = comp_id
        saverecordobj.done_by = request.user.get_full_name()
        saverecordobj.date = datetime.today()
        saverecordobj.remark = request.user.get_full_name() + ' deleted file ' + filename
        saverecordobj.save()
        os.remove(file_path)
        # delete record
        comp_file.delete()
    return redirect('Company_file', pk=comp_id)

def download_file(request,pk):
    getpath = CompanyFile.objects.get(id=pk)
    path = str(getpath.filepath)
    filename = path.split('\\')[-1]
    filepath = open(path, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(path)
    # Set the return value of the HttpResponse
    response = HttpResponse(filepath, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def changePassword(request, pk):
    print('Change password')
    certain_user = User.objects.get(id=pk)
    # print(len(certain_user))
    # if request.user.is_authenticated:
    if request.user.is_anonymous:
        print('lol not again')
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    if request.method == 'POST':
        form = changePasswordForm(request.POST, instance=certain_user)
        # print(form)
        if form.is_valid():
            certain_user.set_password(request.POST.get('password'))
            certain_user.save()
            update_session_auth_hash(request, certain_user)
            return redirect('Ad_User_details')
    else:
        form = changePasswordForm(instance=certain_user)
    return render(request,'userapp/change_password.html', {'form': form, 'base': 'userapp/base.html'})


def aduserPage(request):
    # if request.user.is_authenticated:
    if request.user.is_anonymous:
        messages.error(request, 'Invalid to go without Login !!!')
        return redirect('/')
    if not request.user.is_superuser:
        messages.error(request, 'Only admin can in!')
        logout(request)
        return redirect('/')
    print('User page')
    all_users = User.objects.values().order_by('id')
    print(all_users)
    print(len(all_users))
    print(all_users[0]['username'])
    return render(request,'userapp/admin_user_details.html',{'userlist': all_users, 'base': 'userapp/base.html'})

def create_new_user(request):
    if request.method == "POST":
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "User added!")
            return redirect("Ad_User_details")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CreateNewUserForm()
    return render(request, 'userapp/create_new_user.html', {'form': form, 'base': 'userapp/base.html'})

def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        if u.is_superuser and u.id == request.user.id:
            messages.error(request,'Cannot delete own account!')
        else:
            u.delete()
            messages.success(request, "The user is deleted")

    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
        return redirect("Ad_User_details")

    except Exception as e:
        messages.error(request,e)
        return redirect("Ad_User_details")

    return redirect("Ad_User_details")

def del_item(request, pk):
    try:
        item = Company.objects.get(id=pk)
        companyname = str(item.company_name)
        companyname = companyname.replace(" ", "_")
        locdir = os.path.join(settings.MEDIA_ROOT, companyname)
        print(item)
        print(locdir)
        item.delete()
        messages.success(request, "Company record deleted")
    except Exception as e:
        messages.error(request,e)
        return redirect("Home")
    try:
        if os.path.exists(locdir):
            shutil.rmtree(locdir)
            messages.success(request, "Folder record deleted")
        else:
            messages.error(request, "Folder record not found")
            return redirect("Home")
    except Exception as e:
        messages.error(request, e)
        return redirect("Home")
    return redirect("Home")

def logoutAction(request):
    logout(request)
    messages.success(request, 'You have logged out!')
    return redirect('/')

