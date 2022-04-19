from django.shortcuts import render, redirect

from .models import Stock
from .forms import StockForm

from django.contrib import messages


def home(request):
    import requests
    import json
    
    if request.method == 'POST':
        ticker = request.POST['ticker']

        # pk_017589dbeb4d476cbf44bea58bb46169
        api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/' + ticker + '/quote?token=pk_017589dbeb4d476cbf44bea58bb46169')

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        
        data = {
            'api': api,
        }
        return render(request, 'quotes/home.html', data)
    else:
        return render(request, 'quotes/home.html', {'ticker': 'Enter a ticker symbol above...' })
    


def about(request):
    data = {}
    return render(request, 'quotes/about.html', data)


def add_stock(request):
    import requests
    import json
    
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added correctly"))
            return redirect('add_stock')
        
    else:
        ticker = Stock.objects.all()
        output = []
        
        for ticker_item in ticker:
            # pk_017589dbeb4d476cbf44bea58bb46169
            api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/' + str(ticker_item) + '/quote?token=pk_017589dbeb4d476cbf44bea58bb46169')
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
            
        data = {
            'ticker': ticker,
            'output': output,
            
        }
        
        return render(request, 'quotes/add_stock.html', data)
    
    


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Stock has been deleted!'))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    data = {
        'ticker': ticker
    }
    return render(request, 'quotes/delete_stock.html', data)