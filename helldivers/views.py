from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView

class intro_view(TemplateView):
    template_name = "helldivers/intro.html"

    def get_context_data(self, **kwargs):
        session_id = self.request.session.session_key

        # Ensure the session has been accessed/created
        if session_id is None:
            self.request.session.save()
            session_id = self.request.session.session_key

        context=super().get_context_data(**kwargs)
        context["session_id"]=session_id
        return context

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("<h1>Welcome to the Helldivers Home Page!</h1>")