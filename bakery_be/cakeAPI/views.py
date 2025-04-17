from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CakeSerializer
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

    def put(self, request, pk):
        """Cập nhật thông tin bánh kem theo ID."""
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
        return Response({"error": "Không tìm thấy bánh!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """Xóa bánh kem theo ID."""
        cake = get_object(db.cakes, pk)
        if cake:
            db.cakes.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Xóa bánh thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Không tìm thấy bánh!"}, status=status.HTTP_404_NOT_FOUND)