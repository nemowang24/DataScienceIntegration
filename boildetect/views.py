from django.views.generic import TemplateView

# Create your views here.
class Boil_View(TemplateView):
    template_name = "boildetect/index.html"

class Boil_View_2(TemplateView):
    template_name = "boildetect/index2.html"