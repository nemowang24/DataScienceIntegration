from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm, CustomUserLoginForm

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login3333")
    template_name = "registration/signup.html"

class LoginView(LoginView):
    template_name = "registration/login2.html"
    success_url = reverse_lazy("home")
    form_class =CustomUserLoginForm
    # context = {
    #     "form": "Alice",
    # }
    # return render(request, "pages/about.html", context)
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.pop('request', None)  # Remove the request parameter
    #     return kwargs