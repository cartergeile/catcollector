from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Cat, Toy
from .forms import FeedingForm

# Create your views here.

# Define the home view function
def home(request):
  return render(request, 'home.html')

# about route
def about(request):
  return render(request, 'about.html')

# cats index view
def cats_index(request):
  # We pass data to a template very much like we did in Express!
  # gather relations from SQL using model methods
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', { 'cats': cats })

# detail route for cats
# cat_id is defined, expecting integer, in url
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form })


class CatCreate(CreateView):
  model = Cat
  # the fields attribute is required for a createview
  fields = '__all__'
  # could have also written fields like this:
  # fields = ['name', 'breed', 'description', 'age']

class CatUpdate(UpdateView):
  model = Cat
  # disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'

def add_feeding(request, cat_id):
  # create a ModelForm instance from the data in request.POST
  form = FeedingForm(request.POST)

  # need to validate the form
  if form.is_valid():
    # dont want to save form to db until it has the cat id
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

# ToyList
class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    # define what the inherited is_valid method
    def form_valid(self, form):
        # well use this later for auth
        return super().form_valid(form)
# ToyUpdate
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

# ToyDelete
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'