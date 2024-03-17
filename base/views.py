from django.views import generic
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.conf import settings

# Create your views here.
class UserCreate(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class Login(LoginView):
    def get_success_url(self):
        if self.request.user.type == 'mentee': 
            return reverse_lazy('mentor-list')
        slug = self.request.user.mentor.slug
        return reverse_lazy('mentor-detail', args=[slug])



class VideoCall(generic.TemplateView):
    template_name = 'main/video-call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["appID"] = settings.APP_ID
        context["serverSecret"] = settings.SERVER_SECRET
        return context
 
