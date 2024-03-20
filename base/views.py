from django.views import generic
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.conf import settings

# Create your views here.
class Register(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')



class VideoCall(generic.TemplateView):
    template_name = 'base/video_call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["appID"] = settings.APP_ID
        context["serverSecret"] = settings.SERVER_SECRET
        return context
