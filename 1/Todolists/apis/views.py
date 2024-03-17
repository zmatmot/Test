from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TodolistSerializer
from .models import Todolist


"""

API Overview

"""
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/Todolist-all/',
        'Detail View' : '/Todolist-detail/<str:pk>/',
        'Create' : '/Todolist-create/',
        'Update' : '/Todolist-update/<str:pk>/',
        'Delete' : '/Todolist-delete/<str:pk>/',
    }
    return Response(api_urls)
"""

This function below will show the entire task repository in the database.

"""
@api_view(['GET'])
def todoList(request):
    todoLists = Todolist.objects.all()
    serializer = TodolistSerializer(todoLists, many = True)
    return Response(serializer.data)

"""

This function will show the detailed view of a specific task with the help of pk.

"""
@api_view(['GET'])
def todoListDetail(request, pk):
    todoLists = Todolist.objects.get(id=pk)
    serializer = TodolistSerializer(todoLists, many = False)
    return Response(serializer.data)



@api_view(['POST'])
def todoListCreate(request):
    if request.method == 'GET':
        todoLists = Todolist.objects.all()
        serializer = TodolistSerializer(todoLists, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'completed': request.data.get('completed')
        }
        serializer = TodolistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def todoListUpdate(request, pk):
    todoList = Todolist.objects.get(id = int(pk))
    serializer = TodolistSerializer(instance=todoList, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def todoListDelete(request, pk):
    todoList = Todolist.objects.get(id = pk )
    todoList.delete()
    return Response("Todolist deleted successfully.")