from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get the existing context data
        context = super().get_context_data(**kwargs)

        # Get the session ID (cookie sessionid)
        session_id = self.request.session.session_key

        # Ensure the session is created
        if session_id is None:
            self.request.session.save()
            session_id = self.request.session.session_key

        # Pass the session ID to the context
        context['session_id'] = session_id
        return context