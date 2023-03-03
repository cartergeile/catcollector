from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat


# temporary cats for building templates
# views.py

# Add this cats list below the imports
cats = [
  {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
  {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
  {'name': 'Boots', 'breed': 'calico', 'description': 'shy and cute', 'age': 12},
  {'name': 'Tigger', 'breed': 'tabby', 'description': 'fat and annoying', 'age': 12},
]

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
  return render(request, 'cats/detail.html', { 'cat': cat })


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