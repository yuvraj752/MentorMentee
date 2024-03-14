from django.views import generic
from .models import Message, User
from .forms import UserCreationForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

# Create your views here.
class MessageList(generic.ListView):
    model = Message
    paginate_by = 32

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Message.objects.filter(reciever__pk=pk)

class MessageDetail(generic.DetailView):
    model = Message

    def get_object(self, queryset=None):
        message = super().get_object(queryset)
        if not message.is_read:
            message.is_read = True
            message.save()
        return message
    
class MessageCreate(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('login')
    model = Message
    fields = ['body']
    template_name = 'main/message_create.html'
    success_url = reverse_lazy('mentor-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentor_user = User.objects.get(pk=self.kwargs['pk'])
        context["mentor_user"] = mentor_user
        return context
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        mentor_user = User.objects.get(pk=self.kwargs['pk'])
        form.instance.reciever = mentor_user
        return super().form_valid(form)

class MessageReply(generic.CreateView):
    model = Message
    fields = ['body']
    template_name = 'main/message_reply.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse_lazy('message-list', args=[pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentee = User.objects.get(pk=self.kwargs['pk'])
        context["mentee"] = mentee
        return context
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        mentee = User.objects.get(pk=self.kwargs['pk'])
        form.instance.reciever = mentee
        return super().form_valid(form)

class VideoCall(generic.TemplateView):
    template_name = 'main/video-call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["appID"] = settings.APP_ID
        context["serverSecret"] = settings.SERVER_SECRET
        return context
 
class UserCreate(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class Login(LoginView):
    form_class = LoginForm
    def get_success_url(self):
        if self.request.user.type == 'mentee': 
            return reverse_lazy('mentor-list')
        pk = self.request.user.mentor.pk
        return reverse_lazy('mentor-detail', args=[pk])
