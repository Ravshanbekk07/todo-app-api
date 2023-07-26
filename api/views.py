from django.views import View
from django.http import JsonResponse, HttpRequest
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import User
from .models import Task


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
        data =  json.loads(request.body.decode("utf-8"))
        userid = data.get("author")
        author = User.objects.get(pk=userid)
        if pk is None:
            tasks = Task.objects.filter(author=author).all()
            task_list = [model_to_dict(task) for task in tasks]
            return JsonResponse(task_list,safe=False)
        else:
            try:
                task = Task.objects.get(id=pk, author=author)
                task_dict = model_to_dict(task)
                return JsonResponse(task_dict)
            except User.DoesNotExist:
                return JsonResponse({'error':'user not found'})
            except Task.DoesNotExist:
                return JsonResponse({"error":"task not found "})
    
    def post(self,request):
       
        data = json.loads(request.body.decode('utf-8'))
        try:
            task = Task.objects.create(
                title = data.get('title'),
                description = data.get("description"),
                completed = data.get('completed'),
                author = User.objects.get(id  = data.get('author'))
            )

            return JsonResponse (model_to_dict(task),status =201)
        except KeyError:
            return JsonResponse({'error':'invalid data'})
    def put(self,request,pk=None):
        data = json.loads(request.body.decode("utf-8"))
        userid = data.get("author")
        author = User.objects.get(pk=userid)
        if pk is None:
            return JsonResponse({"error":"invalid data"},status=400)
        try:
            task = Task.objects.get(pk=pk,author = author)
            data = json.loads(request.body.decode("utf-8"))
            task.title = data.get("title")
            task.description  = data.get("description")
            task.completed = data.get("completed")
            task.save()
            return JsonResponse(model_to_dict(task))
        except Task.DoesNotExist:
            return JsonResponse({"error":"Task not found"})
        except KeyError:
            return JsonResponse({"error":"invalid data"})

    def delete(self,request,pk=None):
        data = json.loads(request.body.decode("utf-8"))
        userid = data.get("author")
        author  = User.objects.get(pk=userid)
        if pk is None:

            return JsonResponse({"error":"Invalid data"},status= 400)
        try:
            task = Task.objects.get(id = pk,author=author)
            task.delete()
            return JsonResponse({'status': 'ok'})

        except Task.DoesNotExist:
            return JsonResponse({"error":"Task not found"})

        except User.DoesNotExist:
            return JsonResponse({"error":"user not found"})


