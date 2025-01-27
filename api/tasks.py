from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status, request
import logging
import json
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Clicks


logger = logging.getLogger(__name__)


# @api_view(['POST'])
# @csrf_exempt
# class API_view2(View):
#     @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#         try:
#             # Parse JSON body data from the POST request
#             body = json.loads(request.body)
#             counter_value = body.get('counterValue', 0)  # Default value is 0 if not provided
#
#             # Your business logic here
#             if counter_value == 50:
#                 return JsonResponse({"message": "Success! You hit 50.", "status": "success"}, status=200)
#             else:
#                 return JsonResponse({
#                     "message": f"You clicked at {counter_value}. Try again.",
#                     "status": "failure"
#                 }, status=200)
#         except Exception as e:
#             return JsonResponse({
#                 "error": "Invalid data or server error.",
#                 "details": str(e)
#             }, status=400)

# @api_view(['POST'])
# def api_counter(request):
#     logger.debug("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#
#     if request.method == 'POST':
#         try:
#             # Parse the JSON data sent with the request
#             data = json.loads(request.body)
#             counter_value = data.get('counterValue', None)
#
#             # Validate the counter value
#             if counter_value is None or not isinstance(counter_value, int):
#                 return JsonResponse({'error': 'Invalid counter value provided'}, status=400)
#
#             # Perform any processing you'd like (e.g., save to a database or run logic)
#             # Example: If you want to log success at a specific value
#             if counter_value == 50:
#                 message = "Success! You hit 50!"
#             else:
#                 message = f"Counter value was: {counter_value}"
#
#             # Example: Return a success response with custom message
#             return JsonResponse({'message': message}, status=200)
#
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     else:
#         # Handle non-POST requests
#         return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# curl --header "Content-Type: application/json" --request POST --data '{\"counter\":50}' http://192.168.1.240:8000


class API_view(ViewSet):

    def list(self, request):
        # Placeholder response; adjust to your logic
        return Response({"counter": 123})

    def create(self, request):
        try:
            # Parse JSON body data from the POST request
            body = json.loads(request.body)
            counter_value = body.get('counterValue', 0)  # Default value is 0 if not provided

            session_id = self.request.session.session_key
            if session_id is None:
                self.request.session.save()
                session_id = self.request.session.session_key
            click_db = Clicks(counter=counter_value, sessionid=session_id)
            click_db.save()

            # Your business logic here
            if counter_value == 50:
                return JsonResponse({"message": "Success! You hit 50.", "status": "success"}, status=200)
            else:
                return JsonResponse({
                    "message": f"You clicked at {counter_value}. Try again.",
                    "status": "failure"
                }, status=200)
        except Exception as e:
            return JsonResponse({
                "error": "Invalid data or server error.",
                "details": str(e)
            }, status=400)



    # def create(self, request):
    #     """
    #     Handle POST requests to create a new task.
    #     """
    #     task_data = request.data  # Accessing data sent in the POST request
    #     return Response(
    #         {"message": "Task created successfully!", "data": task_data},
    #         status=status.HTTP_201_CREATED
    #     )