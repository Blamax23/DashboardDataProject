from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.http import HttpResponseRedirect
import csv
from .models import Product, Sale
from django.db.models import Avg
import pandas as pd 
from .utils import Graphs
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request,
    'home.html' ,
    {'date' : datetime. now()})

def logout_view(request):
    logout(request)
    return render(request, 'home.html')

def login_view(request):

    if(request.method == 'POST'):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return render(request, 'home.html')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def performances(request):
    if request.method == 'POST':
        df = pd.json_normalize(list(Sale.objects.all().values()))
        df["product"] = Sale.objects.select_related('product_id').values_list('product__name', flat=True)
        if 'show_chart' in request.POST:
            if(request.POST['datefrom'] != ""):
                datefrom = timezone.make_aware(datetime.strptime(request.POST['datefrom'], '%Y-%m-%d'))
            else:
                datefrom = timezone.make_aware(datetime(1970, 1, 1))

            if(request.POST['dateto'] != ""):
                dateto = request.POST['dateto']
            else:
                dateto = timezone.make_aware(datetime.now())

            df = df[(df['date'] >= datefrom) & (df['date'] <= dateto)]

            if(request.POST['format'] == "Barplot"):
                image = Graphs.get_barplot(df=df)
            elif(request.POST['format'] == "Lineplot"):
                image = Graphs.get_lineplot(df=df)
            elif(request.POST['format'] == "Countplot"):
                image = Graphs.get_countplot(df=df)
            # Le bouton "Show chart" a été cliqué
            return render(request, 'performances.html', {'formats': ["Barplot", "Lineplot", "Countplot"], 'graph': image})
        elif 'summary' in request.POST:
            df = pd.DataFrame({"Price" : list(Sale.objects.all().values())})

            df['Price'] = df['Price'].astype(float)
            count = df['Price'].count()
            mean = df['Price'].mean()
            median = df['Price'].median()
            min = df['Price'].min()
            max = df['Price'].max()
            stdDev = df['Price'].std()
            donnees = {"Donnees": {"Count" : count, "Mean": mean, "Median": median, "Min": min, "Max": max, "StdDev": stdDev}}
            return render(request, 'performances.html', {'formats': ["Barplot", "Lineplot", "Countplot"], 'graph': "", 'donnees': donnees})
    else:
        return render(request, 'performances.html', {'formats': ["Barplot", "Lineplot", "Countplot"], 'graph': ""})

def addsales(request):
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['produit'])
        price = int(request.POST['prix'])
        quantity = int(request.POST['quantite'])
        total_price = price * quantity
        sale = Sale(
            product=product,
            price=price,
            quantity=quantity,
            total_price=total_price,
            seller=request.user
        )
        sale.save()
        return render(request, 'addsales.html', {'products': Product.objects.all()})
    else:
        return render(request, 'addsales.html', {'products': Product.objects.all()})

def uploadFiles(request):

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Lisez le fichier CSV et traitez les données
        decoded_file = uploaded_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_file)

        for row in csv_reader:
            if Product.objects.filter(name=row['Produit']).exists() == False:
                product = Product(name=row['Produit'], date=row['Date'])
                product.save()

            produit = Product.objects.filter(name=row['Produit']).first()

            prix = int(row['Prix'])
            quantite = int(row['Quantite'])
            product = Sale(
                product = produit,
                date = row['Date'],
                price = prix,
                quantity = quantite,
                seller = request.user,
                total_price = prix * quantite,
                )
            
            product.save()

        return render(request, 'uploadFiles.html', {'uploaded_file': uploaded_file})
    else:
        return render(request, 'uploadFiles.html')

def home(request):
    return render(request, 'home.html')
