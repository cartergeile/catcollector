from django.db import models
from django.urls import reverse


# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.


class Cat(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    age = models.IntegerField()

    # dunder str method return cat name
    def __str__(self):
        return self.name
    
    # this is used to direct
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})
    
# Add new Feeding model
class Feeding(models.Model):
    date = models.DateField('Feeding Date')
    meal = models.CharField(
        max_length=1,
        # add choices field
        choices=MEALS,
        #set a default value for meal to be 'B'
        default=MEALS[0][0]
    )
    # create a cat_id foreign key
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"