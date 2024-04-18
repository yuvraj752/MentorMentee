from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import UserCreationForm, LoginForm
from django.urls import reverse_lazy
from .models import User, Mentor, ChatRoom
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import MenteeForm, MentorForm
from django.db.models import Q, Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

# Create your views here.
class Home(ListView):
    model = Mentor
    template_name = "base/home.html"
    queryset = Mentor.objects.filter(approved=True)[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = timezone.now().year 
        return context
    
class Register(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')
    success_message = "Account created successfully."

class Login(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    success_message = 'You are now logged in.'
    template_name = 'auth/login.html'
    
    def get_success_url(self):
        if self.request.user.type == 'mentee': 
            return reverse_lazy('home')
        slug = self.request.user.mentor.slug
        return reverse_lazy('mentor_detail', args=[slug])

class MenteeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = MenteeForm
    template_name = 'base/mentee_form.html'
    success_message = "Profile updated successfully."

    def get_success_url(self):
        return reverse_lazy('home')
    
class MentorSearch(ListView):
    paginate_by = 16
    queryset = Mentor.objects.filter(approved=True)
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return self.queryset.filter(
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
    
class MentorUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
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
        chats = self.get_queryset()
        chats.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        return super().get(request, *args, **kwargs)
    
class ChatRoomList(LoginRequiredMixin, ListView):
    paginate_by = 16
    queryset = ChatRoom.objects.annotate(last_chat_created=Max('chat__created')).order_by('-last_chat_created')

    def get_queryset(self):
        if self.request.user.type == 'mentor':
            username = self.request.user.username + '-'
        else:
            username = '-' + self.request.user.username
        return super().get_queryset().filter(name__contains=username).filter(chat__isnull=False).distinct()
