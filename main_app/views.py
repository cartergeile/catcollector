from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Cat, Toy, Photo
from .forms import FeedingForm
import uuid # python package for creating unique identifiers
import boto3 # use to connect s3
from django.conf import settings

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
def cats_index(request):
  # We pass data to a template very much like we did in Express!
  # gather relations from SQL using model methods
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', { 'cats': cats })

# detail route for cats
# cat_id is defined, expecting integer, in url
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)

  # get a list of ids of toys the cat owns
  id_list = cat.toys.all().values_list('id')
  # get a list of toys cat doesnt have
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)


  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have })


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

def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
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
    success_url = '/toys/'

# view for adding photos
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