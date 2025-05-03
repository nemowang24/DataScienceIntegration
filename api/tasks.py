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
from .models import Clicks, Prompts

logger = logging.getLogger(__name__)


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


class API_saveprompt(ViewSet):
    def list(self, request):
        return Response({"counter": 123})

    def create(self, request):
        try:
            counter_value = request.data.get('counterValue', {})

            # Extract individual values from the dictionary
            resolution = counter_value.get('input1', '(none)')
            quality = counter_value.get('input2', '(none)')
            prompt = counter_value.get('input3', '(none)')
            notes = counter_value.get('input4', '(none)')
            input5 = counter_value.get('input5', '(none)')
            input6 = counter_value.get('input6', '(none)')
            input7 = counter_value.get('input7', '(none)')

            session_id = self.request.session.session_key
            if session_id is None:
                self.request.session.save()
                session_id = self.request.session.session_key

            prompt_db = Prompts(
                model="gpt-image-1",
                resolution=resolution,
                quality=quality,
                prompt=prompt,
                note=notes,
                sessionid=session_id)
            prompt_db.save()

            # Prepare a response
            response_data = {
                'message': 'Data received successfully',
                'inputs': {
                    'input1': resolution,
                    'input2': quality,
                    'input3': prompt,
                    'input4': notes,
                    'input5': input5,
                    'input6': input6,
                    'input7': input7,
                }
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({
                "error": "Invalid data or server error.",
                "details": str(e)
            }, status=400)
