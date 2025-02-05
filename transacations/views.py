from django.shortcuts import render

# Create your views here.


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





@login_required(login_url='login')
def add_investor(request):

    if request.method == 'POST':

        forms = investor_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_investor')
        else:
            context = {
                'form': forms
            }
            return render(request, 'transactions/add_investor.html', context)
    
    else:

        forms = investor_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_investor.html', context)

        

@login_required(login_url='login')
def update_investor(request, investor_id):

    if request.method == 'POST':

        instance = investor.objects.get(id=investor_id)

        forms = investor_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_investor')
        else:
            print(forms.errors)
    
    else:

        instance = investor.objects.get(id=investor_id)
        forms = investor_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_investor.html', context)

        

@login_required(login_url='login')
def delete_investor(request, investor_id):

    investor.objects.get(id=investor_id).delete()

    return HttpResponseRedirect(reverse('list_investor'))


@login_required(login_url='login')
def list_investor(request):

    data = investor.objects.all()
    context = {
        'data': data
    }
    return render(request, 'transactions/list_investor.html', context)


from django.db import IntegrityError

def add_operator(request):
    if request.method == 'POST':
        form = operator_Form(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('list_operator')  # Redirect after successful save
            except IntegrityError:
                form.add_error('username', "This username is already taken. Please choose another.")
                return render(request, 'transactions/add_operator.html', {'form': form}) # Redirect after successful save
        else:
            return render(request, 'transactions/add_operator.html', {'form': form})
    else:
        form = operator_Form()

    return render(request, 'transactions/add_operator.html', {'form': form})




from django.shortcuts import render, get_object_or_404, redirect

@login_required(login_url='login')
def update_operator(request, operator_id):

    operator_instance = get_object_or_404(operator, id=operator_id)

    if request.method == "POST":
        print('---------------------')
        print('---------------------')
        print('---------------------')
        print('---------------------')
        print('---------------------')
        print('---------------------')
        form = operator_Form(request.POST, instance=operator_instance)
        if form.is_valid():
            form.save()
            return redirect('list_operator')  # Redirect after update
    else:
        form = operator_Form(instance=operator_instance)

    return render(request, 'transactions/add_operator.html', {'form': form})

        

@login_required(login_url='login')
def delete_operator(request, operator_id):

    operator.objects.get(id=operator_id).delete()

    return HttpResponseRedirect(reverse('list_operator'))


@login_required(login_url='login')
def list_operator(request):

    data = operator.objects.all()
    context = {
        'data': data
    }
    return render(request, 'transactions/list_operator.html', context)






@login_required(login_url='login')
def add_transactions(request):

    if request.method == 'POST':

        if not request.user.is_superuser:
            updated_params = request.POST.copy()  
        
            operator_instance = operator.objects.get(user = request.user)

            updated_params.update({
                'operator': operator_instance
            })

            forms = transactions_Form(updated_params)


        else:

            forms = transactions_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_transactions')
        else:

            context = {
                'form': forms
            }

            return render(request, 'transactions/add_transactions.html', context)
    
    else:

        forms = transactions_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_transactions.html', context)

        

@login_required(login_url='login')
def update_transactions(request, transactions_id):

    if request.method == 'POST':

        instance = transactions.objects.get(id=transactions_id)
        
        if not request.user.is_superuser:
            updated_params = request.POST.copy()  
        
            operator_instance = operator.objects.get(user = request.user)

            updated_params.update({
                'operator': operator_instance
            })

            forms = transactions_Form(updated_params, instance=instance)


        else:

            forms = transactions_Form(request.POST, instance=instance)


        if forms.is_valid():
            forms.save()
            return redirect('list_transactions')
        else:
            print(forms.errors)
    
    else:

        instance = transactions.objects.get(id=transactions_id)
        forms = transactions_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_transactions.html', context)

        

@login_required(login_url='login')
def delete_transactions(request, transactions_id):

    transactions.objects.get(id=transactions_id).delete()

    return HttpResponseRedirect(reverse('list_transactions'))


@login_required(login_url='login')
def list_transactions(request):

    data = transactions.objects.all()
    context = {
        'data': data
    }
    return render(request, 'transactions/list_transactions.html', context)


from .filters import *

@login_required(login_url='login')
def report(request):

    data = transactions.objects.all().order_by("id")

    filter_data = transactions_filter(request.GET, queryset=data)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(filter_data.qs, 50)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        'data': data,
        'transactions_filter': filter_data,
       
    }

    return render(request, 'transactions/report.html', context)

   






import mimetypes
from django.http import HttpResponse
import csv


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def report_download(request):

    data = transactions.objects.all().order_by("id")

    filter_data = transactions_filter(request.GET, queryset=data)



    
    order_filters_data1 = list(filter_data.qs.values_list('id', 'investor', 'operator', 'timestamp', 'amount', 'remark'))
    order_filters_data = list(map(list, order_filters_data1))
    

    vals = []
        
    vals1 = []

    
    vals.append([''])
    vals.append(['TRANSACTIONS REPORT'])
    vals.append([''])
    vals.append([''])
    
    vals1.append("Sr No")
    vals1.append("Investor")
    vals1.append("Operator")
    vals1.append("Date Time")
    vals1.append("Amount")
    vals1.append("Remark")
    vals.append(vals1)

    counteer = 1

    for i in order_filters_data:
        vals1 = []
        vals1.append(counteer)
        counteer += 1
        vals1.append(i[0])  # Sheet Id
        vals1.append(i[1])  # Sheet Id
        vals1.append(i[2])  # Sheet Id
        vals1.append(i[3])  # Left SQinch
        vals.append(vals1)


    name = "Sales_Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name

    
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)


        link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    with open(path,  'r', newline="") as f:
        mime_type  = mimetypes.guess_type(link)

        response = HttpResponse(f.read(), content_type=mime_type)
        response['Content-Disposition'] = 'attachment;filename=' + str(link)

        return response
