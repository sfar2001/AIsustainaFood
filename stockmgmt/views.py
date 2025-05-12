from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from .services import StockPredictor


def dashboard(request):
    """Main dashboard view"""
    products = Product.objects.all().order_by('-last_predicted')
    context = {
        'products': products,
        'stats': {
            'total_products': products.count(),
            'low_stock': products.filter(stock_urgency='Urgent').count()
        }
    }
    return render(request, 'stockmgmt/dashboard.html', context)


def product_list(request):
    """List all products"""
    products = Product.objects.all().select_related('created_by')
    return render(request, 'stockmgmt/product_list.html', {'products': products})


def add_product(request):
    """Add new product with prediction"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.created_by = request.user

                # Get prediction
                predictor = StockPredictor()
                prediction = predictor.predict({
                    'quantity': product.quantity,
                    'current_stock': product.stock,
                    'min_threshold': product.min_stock,
                    'reorder_qty': product.reorder_qty
                })

                # Update product with prediction results
                product.prediction = prediction['prediction']
                product.confidence = prediction['confidence']
                product.stock_urgency = 'Urgent' if product.stock < product.min_stock else 'Normal'
                product.save()

                messages.success(request, 'Product added successfully with prediction')
                return redirect('product_list')

            except Exception as e:
                messages.error(request, f'Prediction failed: {str(e)}')
    else:
        form = ProductForm()

    return render(request, 'stockmgmt/add_product.html', {'form': form})