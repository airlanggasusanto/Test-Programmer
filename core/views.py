from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
import json
from core.models import Produk, Kategori, Status
from core.forms import ProdukForm

def index(request):
    products = Produk.objects.select_related('kategori', 'status').all()
    categories = Kategori.objects.all()
    return render(request, 'core/index.html', {'products': products, 'categories': categories})

@require_POST
def add_product(request):
    try:
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Invalid content type, JSON required'}, status=400)
        
        data = json.loads(request.body)

        form = ProdukForm(data)
        if not form.is_valid():
            return JsonResponse({'error': form.errors}, status=400)

        kategori = get_object_or_404(Kategori, id=data['kategori'])
        status = get_object_or_404(Status, id=data['status'])

        new_product = Produk.objects.create(
            nama_produk=data['nama_produk'],
            kategori=kategori,
            harga=data['harga'],
            status=status
        )
        return JsonResponse({'message': 'Product added successfully', 'id': new_product.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)


@require_POST
def delete_product(request):
    try:
        data = json.loads(request.body)
        
        product_id = data.get("product_id")  # Extract product_id from body
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)

        product = get_object_or_404(Produk, id=product_id)
        product.delete()

        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def get_product(request, product_id):
    try:
        product = get_object_or_404(Produk.objects.select_related('kategori', 'status'), id=product_id)
        return JsonResponse({
            'id': product.id,
            'nama_produk': product.nama_produk,
            'kategori': {'id': product.kategori.id, 'nama_kategori': product.kategori.nama_kategori},
            'harga': product.harga,
            'status': {'id': product.status.id, 'nama_status': product.status.nama_status},
        })
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

@require_POST
def update_product(request):
    try:
        if request.content_type != "application/json":
            return JsonResponse({"error": "Invalid content type, JSON required"}, status=400)

        data = json.loads(request.body)

        product_id = data.get("product_id")
        if not product_id:
            return JsonResponse({"error": "Missing product_id in request"}, status=400)

        product = get_object_or_404(Produk, id=product_id)

        form = ProdukForm(data, instance=product)
        if not form.is_valid():
            return JsonResponse({"error": form.errors}, status=400)

        kategori = get_object_or_404(Kategori, id=data["kategori"])
        status = get_object_or_404(Status, id=data["status"])

        product.nama_produk = data["nama_produk"]
        product.kategori = kategori
        product.harga = data["harga"]
        product.status = status
        product.save()

        return JsonResponse({"message": "Product updated successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)
