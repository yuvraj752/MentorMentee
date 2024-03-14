from django.views import generic
from .models import Mentor
from django.db.models import Q
from django.urls import reverse_lazy

# Create your views here.
class MentorList(generic.ListView):
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

class MentorDetail(generic.DetailView):
    model = Mentor

class MentorEdit(generic.UpdateView):
    model = Mentor
    fields = ('name', 'image', 'email', 'job_title', 
              'price', 'category', 'skill', 'description')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control my-2'})
        return form

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('mentor-detail', args=[pk])