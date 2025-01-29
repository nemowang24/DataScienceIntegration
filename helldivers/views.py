from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import matplotlib.pyplot as plt
from django.http import FileResponse
import os
from rest_framework.decorators import api_view
from rest_framework import status, request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api.models import Clicks
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

logger = logging.getLogger(__name__)


class Intro_view(TemplateView):
    template_name = "helldivers/intro.html"

    def get_context_data(self, **kwargs):
        session_id = self.request.session.session_key

        # Ensure the session has been accessed/created
        if session_id is None:
            self.request.session.save()
            session_id = self.request.session.session_key

        context = super().get_context_data(**kwargs)
        context["session_id"] = session_id
        return context


class Practice_view(TemplateView):
    template_name = "helldivers/shooting_practice.html"

class Statistic_view(TemplateView):
    template_name = "helldivers/statistic.html"

    def generate_histogram(self):
        # Extract data from Clicks table
        data = Clicks.objects.values_list('counter', flat=True)

        plt.figure(figsize=(20, 12))
        plt.hist(data, bins=100, color='blue', alpha=0.7)
        plt.title('Clicks Distribution')
        plt.xlabel('Counter Value')
        plt.ylabel('Frequency')

        # Set major ticks (already in the code, every 5)
        plt.xticks(ticks=range(0, 100, 5), rotation=45)

        # Add minor ticks (e.g., every 1)
        ax = plt.gca()  # Get current axis
        ax.xaxis.set_minor_locator(MultipleLocator(1))  # Sub ticks every 1 unit
        ax.tick_params(axis='x', which='minor', length=4, color='red')  # Customize minor ticks (optional)

        # Show grid with minor ticks if desired
        ax.grid(visible=True, which='both', axis='x', linestyle='--', color='gray', alpha=0.7)

        # Save or show the plot
        file_path = os.path.join('media', 'histogram.png')
        plt.savefig(file_path)
        plt.close()

        return file_path

    # def get(self, request, *args, **kwargs):
    #     # First, generate the histogram
    #     file_path = self.generate_histogram()
    #
    #     # Return the file as a response
    #     return FileResponse(open(file_path, 'rb'), content_type='image/png')

    def get_context_data(self, **kwargs):
        file_path = self.generate_histogram()
        # Get the existing context
        context = super().get_context_data(**kwargs)
        # Add the file path as a variable to the context
        context["file_path"] = file_path
        return context



# class API_view(View):
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

# @csrf_exempt
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
#
#
# class TaskViewSet2(ViewSet):
#     def api_counter(request):
#         logger.debug("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#         if request.method == 'POST':
#             try:
#                 # Parse the JSON data sent with the request
#                 data = json.loads(request.body)
#                 counter_value = data.get('counterValue', None)
#
#                 # Validate the counter value
#                 if counter_value is None or not isinstance(counter_value, int):
#                     return JsonResponse({'error': 'Invalid counter value provided'}, status=400)
#
#                 # Perform any processing you'd like (e.g., save to a database or run logic)
#                 # Example: If you want to log success at a specific value
#                 if counter_value == 50:
#                     message = "Success! You hit 50!"
#                 else:
#                     message = f"Counter value was: {counter_value}"
#
#                 # Example: Return a success response with custom message
#                 return JsonResponse({'message': message}, status=200)
#
#             except json.JSONDecodeError:
#                 return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         else:
#             # Handle non-POST requests
#             return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
#
#     def create(self, request):
#         # Example implementation for POST /api/counter/
#         return Response(
#             {"message": "Task created successfully"},
#             status=status.HTTP_201_CREATED
#         )
#
#     # @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         logger.debug("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
#         try:
#             # Parse data from the request body
#             data = json.loads(request.body)
#             counter_value = data.get('counterValue', None)
#
#             # Process the counter value (you can add your logic here)
#             print(f"Received counter value: {counter_value}")
#
#             # Return a JSON response back to the client
#             return JsonResponse({'message': f'Counter value {counter_value} received successfully.'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': 'Invalid request data', 'details': str(e)}, status=400)


# class TaskViewSet(ViewSet):
#     """
#     ViewSet to handle custom operations for the /api/counter/ endpoint.
#     """
#
#     def list(self, request):
#         """
#         Handle GET requests to return a list of tasks.
#         """
#         return Response({"message": "This is a list of tasks."})
#
#     def create(self, request):
#         """
#         Handle POST requests to create a new task.
#         """
#         task_data = request.data  # Accessing data sent in the POST request
#         return Response(
#             {"message": "Task created successfully!", "data": task_data},
#             status=status.HTTP_201_CREATED
#         )
