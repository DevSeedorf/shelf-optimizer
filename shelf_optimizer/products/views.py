from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from .models import ShelfAllocation, OptimizationResult
from .optimizer import harmony_search, tabu_search
import time

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def optimize_shelves(request):

    method = request.GET.get('method', 'harmony')

    start_time = time.time()

    previous_positions = {
        alloc.product_id: (alloc.shelf, alloc.column)
        for alloc in ShelfAllocation.objects.all()
    }

    if method == 'harmony':
        best_solution, fitness_score, penalty_log = harmony_search(previous_positions)
    else:
        best_solution, fitness_score, penalty_log = tabu_search(previous_positions)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)  # ⏱ In seconds

    OptimizationResult.objects.create(
        method=method,
        fitness_score=fitness_score,
        penalty_log="\n".join(penalty_log),
        time_taken=elapsed_time
    )

    context = {
        'allocations': ShelfAllocation.objects.all(),
        'fitness_score': fitness_score,
        'penalty_log': penalty_log,
        'method': method,
    }

    return render(request, 'shelf_allocation.html', {
        'allocations': ShelfAllocation.objects.all(),
        'fitness_score': fitness_score,
        'penalty_log': penalty_log
    })


def shelf_allocation(request):
    allocations = ShelfAllocation.objects.all()
    return render(request, 'shelf_allocation.html', {'allocations': allocations})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')  # Redirect to the shelf allocation page

def optimization_history(request):
    results = OptimizationResult.objects.order_by('-created_at')[:50]  # latest 50 results
    return render(request, 'optimization_history.html', {
        'results': results
    })

def clear_optimization_history(request):
    OptimizationResult.objects.all().delete()
    messages.success(request, "✅ All optimization history has been cleared.")
    return redirect('optimization_history')