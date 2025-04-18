from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CakeSerializer, CategorySerializer, OrderSerializer, PaymentSerializer, UserSerializer
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')  # Lấy MONGO_URI từ settings.py
db = client.QuanLyWebBanBanh  # Tên database

def home(request):
    return render(request, 'cake/home.html')

# --- Helper Function ---
def get_object(collection, pk):
    """Lấy một document theo _id."""
    try:
        return collection.find_one({'_id': ObjectId(pk)})
    except:
        return None
        raise

# --- Cake List View ---
class CakeListView(APIView):
    def get(self, request):
        """Lấy danh sách tất cả bánh kem."""
        cakes = list(db.cakes.find())
        for cake in cakes:
            cake["_id"] = str(cake["_id"])  # Chuyển ObjectId thành string
            cake["category_id"] = str(cake["category_id"])
        serializer = CakeSerializer(cakes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Tạo một bánh kem mới."""
        serializer = CakeSerializer(data=request.data)
        if serializer.is_valid():
            new_cake = {
                "name": serializer.validated_data["name"],
                "description": serializer.validated_data["description"],
                "price": serializer.validated_data["price"],
                "image": serializer.validated_data["image"],
                "category_id": serializer.validated_data["category_id"]
            }
            result = db.cakes.insert_one(new_cake)
            new_cake["_id"] = str(result.inserted_id)
            new_cake["category_id"] = str(new_cake["category_id"])
            return Response(CakeSerializer(new_cake).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CakeDetailView(APIView):
    """Lấy, cập nhật hoặc xóa một bánh kem."""

    def get(self, request, pk):
        cake = get_object(db.cakes, pk)
        if cake:
            cake["_id"] = str(cake["_id"])
            cake["category_id"] = str(cake["category_id"])
            serializer = CakeSerializer(cake)
            return Response(serializer.data)
        return Response({"error": "Không tìm thấy bánh kem!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        cake = get_object(db.cakes, pk)
        if cake:
            serializer = CakeSerializer(data=request.data)
            if serializer.is_valid():
                updated_cake = {
                    "name": serializer.validated_data["name"],
                    "description": serializer.validated_data["description"],
                    "price": serializer.validated_data["price"],
                    "image": serializer.validated_data["image"],
                    "category_id": serializer.validated_data["category_id"]
                }
                db.cakes.update_one({"_id": ObjectId(pk)}, {"$set": updated_cake})
                updated_cake["_id"] = pk
                updated_cake["category_id"] = str(updated_cake["category_id"])
                return Response(CakeSerializer(updated_cake).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy bánh kem!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        cake = get_object(db.cakes, pk)
        if cake:
            db.cakes.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Xóa bánh kem thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Không tìm thấy bánh kem!"}, status=status.HTTP_404_NOT_FOUND)
class CategoryListView(APIView):
    def get(self, request):
        """Lấy danh sách tất cả danh mục."""
        categories = list(db.categories.find())
        for category in categories:
            category["_id"] = str(category["_id"])
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Tạo danh mục mới."""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = {
                "name": serializer.validated_data["name"]
            }
            result = db.categories.insert_one(new_category)
            new_category["_id"] = str(result.inserted_id)
            return Response(CategorySerializer(new_category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Category Detail View ---
class CategoryDetailView(APIView):
    """Lấy, cập nhật hoặc xóa một danh mục."""

    def get(self, request, pk):
        category = get_object(db.categories, pk)
        if category:
            category["_id"] = str(category["_id"])
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return Response({"error": "Không tìm thấy danh mục!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        category = get_object(db.categories, pk)
        if category:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                updated_category = {
                    "name": serializer.validated_data["name"]
                }
                db.categories.update_one({"_id": ObjectId(pk)}, {"$set": updated_category})
                updated_category["_id"] = pk
                return Response(CategorySerializer(updated_category).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy danh mục!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        category = get_object(db.categories, pk)
        if category:
            db.categories.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Xóa danh mục thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Không tìm thấy danh mục!"}, status=status.HTTP_404_NOT_FOUND)
class UserListView(APIView):
    def get(self, request):
        """Lấy danh sách tất cả người dùng."""
        users = list(db.users.find())
        for user in users:
            user["_id"] = str(user["_id"])  # Chuyển ObjectId thành string
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Tạo người dùng mới."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = {
                "name": serializer.validated_data["name"],
                "email": serializer.validated_data["email"],
                "password": serializer.validated_data["password"],
                "phone": serializer.validated_data["phone"]
            }
            result = db.users.insert_one(new_user)
            new_user["_id"] = str(result.inserted_id)
            return Response(UserSerializer(new_user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, pk):
        user = get_object(db.users, pk)
        if user:
            user["_id"] = str(user["_id"])
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"error": "Không tìm thấy người dùng!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = get_object(db.users, pk)
        if user:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                updated_user = {
                    "name": serializer.validated_data["name"],
                    "email": serializer.validated_data["email"],
                    "password": serializer.validated_data["password"],
                    "phone": serializer.validated_data["phone"]
                }
                db.users.update_one({"_id": ObjectId(pk)}, {"$set": updated_user})
                updated_user["_id"] = pk
                return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy người dùng!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = get_object(db.users, pk)
        if user:
            db.users.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Xóa người dùng thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Không tìm thấy người dùng!"}, status=status.HTTP_404_NOT_FOUND)
class PaymentListView(APIView):
    def get(self, request):
        """Lấy danh sách tất cả thanh toán."""
        payments = list(db.payments.find())
        for payment in payments:
            payment["_id"] = str(payment["_id"])
            payment["order_id"] = str(payment["order_id"])
            payment["created_at"] = payment["created_at"].isoformat()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Tạo một thanh toán mới."""
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            new_payment = {
                "order_id": ObjectId(serializer.validated_data["order_id"]),
                "amount": serializer.validated_data["amount"],
                "method": serializer.validated_data["method"],
                "status": serializer.validated_data["status"],
                "created_at": serializer.validated_data["created_at"],
            }
            result = db.payments.insert_one(new_payment)
            new_payment["_id"] = str(result.inserted_id)
            new_payment["order_id"] = str(new_payment["order_id"])
            new_payment["created_at"] = new_payment["created_at"].isoformat()
            return Response(PaymentSerializer(new_payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(APIView):
    """Lấy, cập nhật hoặc xóa một thanh toán."""

    def get(self, request, pk):
        payment = get_object(db.payments, pk)
        if payment:
            payment["_id"] = str(payment["_id"])
            payment["order_id"] = str(payment["order_id"])
            payment["created_at"] = payment["created_at"].isoformat()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        payment = get_object(db.payments, pk)
        if payment:
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                updated_payment = {
                    "order_id": ObjectId(serializer.validated_data["order_id"]),
                    "amount": serializer.validated_data["amount"],
                    "method": serializer.validated_data["method"],
                    "status": serializer.validated_data["status"],
                    "created_at": serializer.validated_data["created_at"],
                }
                db.payments.update_one({"_id": ObjectId(pk)}, {"$set": updated_payment})
                updated_payment["_id"] = pk
                updated_payment["order_id"] = str(updated_payment["order_id"])
                updated_payment["created_at"] = updated_payment["created_at"].isoformat()
                return Response(PaymentSerializer(updated_payment).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        payment = get_object(db.payments, pk)
        if payment:
            db.payments.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Xóa thanh toán thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)
class OrderListView(APIView):
    def get(self, request):
        """Lấy danh sách tất cả đơn hàng."""
        orders = list(db.orders.find())
        for order in orders:
            order["_id"] = str(order["_id"])
            order["user_id"] = str(order["user_id"])
            for item in order["items"]:
                item["cake_id"] = str(item["cake_id"])
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Tạo một đơn hàng mới."""
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            new_order = serializer.validated_data
            new_order["user_id"] = ObjectId(new_order["user_id"])
            for item in new_order["items"]:
                item["cake_id"] = ObjectId(item["cake_id"])
            result = db.orders.insert_one(new_order)
            new_order["_id"] = str(result.inserted_id)
            new_order["user_id"] = str(new_order["user_id"])
            for item in new_order["items"]:
                item["cake_id"] = str(item["cake_id"])
            return Response(OrderSerializer(new_order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrderDetailView(APIView):
    """Lấy, cập nhật hoặc xóa một đơn hàng."""

    def get(self, request, pk):
        order = db.orders.find_one({"_id": ObjectId(pk)})
        if order:
            order["_id"] = str(order["_id"])
            order["user_id"] = str(order["user_id"])
            for item in order["items"]:
                item["cake_id"] = str(item["cake_id"])
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response({"error": "Không tìm thấy đơn hàng!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        order = db.orders.find_one({"_id": ObjectId(pk)})
        if order:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                updated_order = serializer.validated_data
                updated_order["user_id"] = ObjectId(updated_order["user_id"])
                for item in updated_order["items"]:
                    item["cake_id"] = ObjectId(item["cake_id"])
                db.orders.update_one({"_id": ObjectId(pk)}, {"$set": updated_order})
                updated_order["_id"] = pk
                updated_order["user_id"] = str(updated_order["user_id"])
                for item in updated_order["items"]:
                    item["cake_id"] = str(item["cake_id"])
                return Response(OrderSerializer(updated_order).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy đơn hàng!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        order = db.orders.find_one({"_id": ObjectId(pk)})
        if order:
            db.orders.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Xóa đơn hàng thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Không tìm thấy đơn hàng!"}, status=status.HTTP_404_NOT_FOUND)