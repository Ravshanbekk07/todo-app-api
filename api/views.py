from django.views import View
from django.http import JsonResponse, HttpRequest
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import User
from .models import Task
from base64 import b64decode
from django.contrib.auth import authenticate

class UsersView(View):
    def get(self, request: HttpRequest, pk=None):
        if pk is None:
            users = User.objects.all()
            users_list = [model_to_dict(user, fields=['id', 'username']) for user in users]
            return JsonResponse(users_list, safe=False)
        else:
            try:
                user = User.objects.get(pk=pk)
                user_dict = model_to_dict(user, fields=['id', 'username'])
                return JsonResponse(user_dict)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            
    def post(self, request: HttpRequest):
        data = request.body.decode('utf-8')
        data = json.loads(data)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user_dict = model_to_dict(user, fields=['id', 'username'])
            return JsonResponse(user_dict, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        
    def put(self, request: HttpRequest, pk=None):
        if pk is None:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        try:
            user = User.objects.get(pk=pk)
            data = request.body.decode('utf-8')
            data = json.loads(data)
            user.username = data['username']
            user.save()
            user_dict = model_to_dict(user, fields=['id', 'username'])
            return JsonResponse(user_dict)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    def delete(self, request: HttpRequest, pk=None):
        if pk is None:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    

class TaskView(View):
    def get(self,request,pk = None):
        headers = request.headers

        authorization = headers.get('Authorization')

        authorization = authorization.split(' ')

        username, password = b64decode(authorization[1]).decode("utf-8").split(':')

        user = authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({"error":"invalid credentials"},status =401)
        if pk is None:
            tasks = Task.objects.filter(author=user).all()
            task_list = [model_to_dict(task,fields=['id','title','completed']) for task in tasks]
            return JsonResponse(task_list,safe=False)
        else:
            try:
                task = Task.objects.get(id=pk, author=user)
                task_dict = model_to_dict(task,fields=['id','title','completed',"description"])
                return JsonResponse(task_dict)
            except User.DoesNotExist:
                return JsonResponse({'error':'user not found'})
            except Task.DoesNotExist:
                return JsonResponse({"error":"task not found"},status=404)
            
    
    def post(self,request):
        headers = request.headers

        authorization = headers.get("Authorization")

        authorization =authorization.split(' ')

        username, password = b64decode(authorization[1]).decode("utf-8").split(':')

        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":'invalid credentials'},status =401)
        
        data = json.loads(request.body.decode("utf-8"))
        try:
            task = Task.objects.create(
                title = data.get('title'),
                description = data.get("description",''),
                completed = data.get('completed',False),
                author = user
            )
            task.save()

            return JsonResponse (model_to_dict(task,fields=['id','title','completed',"description"]),status =201)
        except KeyError:
            return JsonResponse({'error':'invalid data'})
    
        except User.DoesNotExist:
            return JsonResponse({"error":"user not found"},status = 404)
    
    def put(self,request,pk=int):
        headers = request.headers
        authorization = headers.get("Auzorization")
        authorization = authorization.split(' ')
        username,password =b64decode(authorization[1]).decode('utf-8').split(':')

        user = authenticate(username=username,pasword=password)
        if user is None:
            return JsonResponse({"error":"invalid credentials"})
        if pk is None:
            return JsonResponse({"error":"invalid data"},status=400)
        try:
            data = json.loads(request.body.decode("utf-8"))

            task = Task.objects.get(id=pk,author = user)
            task.title = data.get("title",task.title)
            task.description  = data.get("description",task.description)
            task.completed = data.get("completed",task.completed)
            task.save()
            return JsonResponse(model_to_dict(task,fields=["id","title","completed","description"]))
        except Task.DoesNotExist:
            return JsonResponse({"error":"Task not found"})
        except KeyError:
            return JsonResponse({"error":"invalid data"})

    def delete(self,request,pk=int):
        headers = request.headers
        authorization = headers.get("Authorization")
        authorization = authorization.split(" ")
        username,password = b64decode(authorization[1]).decode('utf-8').split(":")
        user = authenticate(username=username,password=password)
        if user is None:

            return JsonResponse({"error":"Invalid credentials"},status= 401)
        try:
            task = Task.objects.get(id = pk,author=user)
            task.delete()
            return JsonResponse({'status': 'ok'})

        except Task.DoesNotExist:
            return JsonResponse({"error":"Task not found"})

        

class LoginView(View):
    def post(self,request:HttpRequest):
        headers = request.headers

        authorization = headers.get("Authorization")
        authorization = authorization.split(' ')

        username, password  = b64decode(authorization[1]).decode("utf-8").split(":")

        try:
            user:User = authenticate(username=username,password=password)

            if user is not None:
                return JsonResponse({"status":"OK"})
            else:
                return JsonResponse({"error":"invalid credentials"},status = 401)
        except KeyError:
            return JsonResponse({"error":"invalid data"},status = 400)
            

