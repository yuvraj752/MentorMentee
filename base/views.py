from django.views import generic
from .forms import UserCreationForm, LoginForm
from django.urls import reverse_lazy
from django.conf import settings
from mentors.models import Mentor
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView

# Create your views here.
class Home(generic.ListView):
    model = Mentor
    template_name = "base/home.html"
    queryset = Mentor.objects.filter(
        approved=True).order_by('created')[:4]

class Register(SuccessMessageMixin, generic.CreateView):
    form_class = UserCreationForm
    template_name = 'base/auth/register.html'
    success_url = reverse_lazy('login')
    success_message = "Account created successfully."

class Login(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'base/auth/login.html'
    success_message = 'You are now logged in'
    def get_success_url(self):
        if self.request.user.type == 'mentee': 
            return reverse_lazy('home')
        slug= self.request.user.mentor.slug
        return reverse_lazy('mentor_detail', args=[slug])

class Chat(generic.TemplateView):
    template_name = "base/chat.html"
    
class VideoCall(generic.TemplateView):
    template_name = 'base/video_call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["appID"] = settings.APP_ID
        context["serverSecret"] = settings.SERVER_SECRET
        return context
