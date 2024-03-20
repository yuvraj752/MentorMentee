from django.views import generic
from .models import Mentor
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import MentorForm

# Create your views here.
class MentorSearch(generic.ListView):
    paginate_by = 32
    queryset = Mentor.objects.filter(approved=True).order_by('created')

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

class MentorDetail(generic.DetailView):
    model = Mentor

class MentorFormView(SuccessMessageMixin, generic.UpdateView):
    model = Mentor
    form_class = MentorForm
    success_message = "Profile updated successfully."
    
    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('mentor_detail', args=[slug])
