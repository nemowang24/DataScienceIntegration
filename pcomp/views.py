from django.views.generic import TemplateView

class PromptInputView(TemplateView):
    template_name = 'pcomp/prompt_input.html'