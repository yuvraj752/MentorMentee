from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView
from .forms import UserCreationForm, LoginForm
from django.urls import reverse_lazy
from .models import Mentor, User, Chat
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import MentorForm
from django.db.models import Q

# Create your views here.
class Home(ListView):
    model = Mentor
    template_name = "base/home.html"
    queryset = Mentor.objects.filter(approved=True)[:4]

class Register(SuccessMessageMixin, CreateView):
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
        slug = self.request.user.mentor.slug
        return reverse_lazy('mentor_detail', args=[slug])

class MentorSearch(ListView):
    paginate_by = 32
    queryset = Mentor.objects.filter(approved=True)

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return self.queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(job_title__icontains=query) | 
                Q(category__icontains=query) | 
                Q(skill__icontains=query))
        return self.queryset

class MentorDetail(DetailView):
    model = Mentor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = f'{self.object.user.username}-{self.request.user.username}'
        context["room"] = room 
        return context
    
class MentorForm(SuccessMessageMixin, UpdateView):
    model = Mentor
    form_class = MentorForm
    success_message = "Profile updated successfully."
    
    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('mentor_detail', args=[slug])

class ChatView(TemplateView):
    template_name = "base/chat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.kwargs['room']
        username = room.split('-')[0]
        context["username"] = self.request.user.username
        context["mentor"] = User.objects.get(username=username)
        context["chats"] = Chat.objects.filter(room=room)
        return context
