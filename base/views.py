from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import UserCreationForm, LoginForm
from django.urls import reverse_lazy
from .models import Mentor, ChatRoom
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import MentorForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(ListView):
    model = Mentor
    template_name = "base/home.html"
    queryset = Mentor.objects.filter(approved=True)[:4]

class Register(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Account created successfully."

class Login(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    success_message = 'You are now logged in.'
    
    def get_success_url(self):
        if self.request.user.type == 'mentee': 
            return reverse_lazy('home')
        slug = self.request.user.mentor.slug
        return reverse_lazy('mentor_detail', args=[slug])

class MentorSearch(ListView):
    paginate_by = 32

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Mentor.objects.filter(approved=True).filter(
                Q(name__icontains=query) | Q(description__icontains=query) | 
                Q(job_title__icontains=query) | Q(category__icontains=query) | 
                Q(skill__icontains=query)
            )
        return self.queryset

class MentorDetail(DetailView):
    model = Mentor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_room = f'{self.object.user.username}-{self.request.user.username}'
        context["chat_room"] = chat_room 
        return context
    
class MentorForm(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Mentor
    form_class = MentorForm
    success_message = "Profile updated successfully."
    
    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('mentor_detail', args=[slug])

class ChatList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        chat_room, _ = ChatRoom.objects.get_or_create(name=self.kwargs['chat_room'])
        return chat_room.chat_set.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender_username = self.request.user.username
        mentor_username = self.kwargs['chat_room'].split('-')[0]
        mentee_username = self.kwargs['chat_room'].split('-')[1]
        context["chat_room"] = self.kwargs['chat_room']
        context["mentor_username"] = mentor_username
        context["sender_username"] = sender_username
        if sender_username == mentor_username:
            context["reciever_username"] = mentee_username
        else:
            context["reciever_username"] = mentor_username
        return context
    
    def get(self, request, *args, **kwargs):
        chat_room = ChatRoom.objects.get(name=self.kwargs['chat_room'])
        chat_room.chat_set.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        return super().get(request, *args, **kwargs)
    
class ChatRoomList(LoginRequiredMixin, ListView):
    paginate_by = 16

    def get_queryset(self):
        username = self.request.user.username
        return ChatRoom.objects.filter(name__contains=username).filter(chat__isnull=False).distinct()
