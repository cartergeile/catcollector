from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Cat, Toy, Photo
from .forms import FeedingForm
import uuid # python package for creating unique identifiers
import boto3 # use to connect s3
from django.conf import settings
# imports for signing up
# want to automatically log in signed up users
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL

# Create your views here.

# Define the home view function
def home(request):
  return render(request, 'home.html')

# about route
def about(request):
  return render(request, 'about.html')

# cats index view
@login_required
def cats_index(request):
  # We pass data to a template very much like we did in Express!
  # gather relations from SQL using model methods
  # cats = Cat.objects.all()
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', { 'cats': cats })

# detail route for cats
# cat_id is defined, expecting integer, in url
@login_required
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)

  # get a list of ids of toys the cat owns
  id_list = cat.toys.all().values_list('id')
  # get a list of toys cat doesnt have
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)

  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have })


class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  # the fields attribute is required for a createview
  # fields = '__all__'
  # could have also written fields like this:
  fields = ['name', 'breed', 'description', 'age']
  def form_valid(self, form):
      # assign the logged in user's data(id) to the cats create form
      form.instance.user = self.request.user
      return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  # disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin,  DeleteView):
  model = Cat
  success_url = '/cats'

@login_required
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

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

# ToyList
class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'color']

    # define what the inherited is_valid method
    def form_valid(self, form):
        # well use this later for auth
        return super().form_valid(form)
# ToyUpdate
class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

# ToyDelete
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

# view for adding photos
@login_required
def add_photo(request, cat_id):
    # photo-file will be name attribute of form input
    photo_file = request.FILES.get('photo-file', None)
    # use conditional logic to make sure a file is present
    if photo_file:
        # if present use this to create reference to the boto3 client
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # create unique key for photos
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # try...except to handle if something goes wrong
        try:
            # if success
            s3.upload_fileobj(photo_file, S3_BUCKET, key)
            # build full url string to upload to s3
            url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"
            # if upload (that used boto3) was successful, use photo location to create a photo model
            photo = Photo(url=url, cat_id=cat_id)
            # save instance to the db
            photo.save()
        except Exception as error:
            # print error message
            print('Error uploading photo', error)
            return redirect('detail', cat_id=cat_id)
    # upon success redirect to detail page
    return redirect('detail', cat_id=cat_id)

# view for signup
def signup(request):
    # just like class based views
    # going to be able to handle a GET and POST request
    error_message = ''
    if request.method == 'POST':
        # how to create a user form object that includes data from the browser
        form = UserCreationForm(request.POST)
        # check validitity of form, handle success and error situations
        if form.is_valid():
            # add user to the database
            user = form.save()
            # then log the user in
            login(request, user)
            # redirect to index page
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # a bad POST or GET request will render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)