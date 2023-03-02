from django.shortcuts import render

# temporary cats for building templates
# views.py

# Add this cats list below the imports
cats = [
  {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
  {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
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
  return render(request, 'cats/index.html', {
    'cats': cats
  })