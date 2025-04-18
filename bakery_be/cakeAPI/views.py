from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CakeSerializer, CategorySerializer
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')  # Lấy MONGO_URI từ settings.py
db = client.QuanLyWebBanBanh  # Tên database

# --- Helper Function ---
def get_object(collection, pk):
    """Lấy một document theo _id."""
    try:
        return collection.find_one({'_id': ObjectId(pk)})
    except:
        return None

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