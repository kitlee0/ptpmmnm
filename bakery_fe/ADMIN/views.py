from django.shortcuts import redirect, render
import requests

# View danh sách bánh kem
from django.shortcuts import redirect, render
import requests

# View danh sách bánh kem
def admin_cakes_view(request):
    # Gọi API để lấy danh sách bánh kem
    response = requests.get("http://localhost:8000/api/cakes/")
    cakes = response.json() if response.status_code == 200 else []
    return render(request, 'admin.html', {'cakes': cakes})

# Xóa bánh kem
def admin_delete_cake(request, cake_id):
    response = requests.delete(f"http://localhost:8000/api/cakes/{cake_id}/")
    if response.status_code == 204:
        return redirect('admin_cakes')
    else:
        return render(request, 'admin.html', {'error': 'Không thể xóa bánh kem.'})

# Sửa bánh kem
def admin_edit_cake(request, cake_id):
    if request.method == 'POST':
        data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "price": int(request.POST.get("price")),
            "image": request.POST.get("image"),
            "category_id": request.POST.get("category_id")
        }
        response = requests.put(f"http://localhost:8000/api/cakes/{cake_id}/", json=data)
        if response.status_code == 200:
            return redirect('admin_cakes')  # Sau khi sửa thành công

    response = requests.get(f"http://localhost:8000/api/cakes/{cake_id}/")
    cake = response.json()
    return render(request, 'edit_cake.html', {'cake': cake})

# Thêm bánh kem mới
def admin_add_cake(request):
    if request.method == 'POST':
        data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "price": int(request.POST.get("price")),
            "image": request.POST.get("image"),
            "category_id": request.POST.get("category_id")
        }
        response = requests.post("http://localhost:8000/api/cakes/", json=data)
        if response.status_code == 201:
            return redirect('admin_cakes')  # Sau khi thêm thành công, quay lại danh sách bánh kem.

    return render(request, 'add_cake.html')  # Form để thêm bánh kem
