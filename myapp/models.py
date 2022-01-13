from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12,blank=False)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic,related_name='courses',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(100.00,  message= 'Price must be greater than 100.00 !!'),
                                                                             MaxValueValidator(200.00,   message= 'Price must be less than 200.00 !!')])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)
    hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Student(User):
    LVL_CHOICES = [
        ('HS','High School'),
        ('UG','Undergraduate'),
        ('PG','Postgraduate'),
        ('ND','No Degree')
    ]

    level = models.CharField(choices=LVL_CHOICES,max_length=2,default='HS')
    address = models.CharField(max_length=300,blank=True)
    province = models.CharField(max_length=2,default='ON')
    registered_courses = models.ManyToManyField(Course,blank=True)
    interested_in = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to='media', blank=True)


    def __str__(self):
        return self.first_name + " " + self.last_name

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0,'Cancelled'),
        (1,'Confirmed'),
        (2,'On Hold')
    ]
    courses = models.ManyToManyField(Course)
    Student = models.ForeignKey(Student,on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES,default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.Student.first_name + " " + self.Student.last_name + " " + str(self.order_date)

    def total_cost(self):
        total = 0
        for course in self.courses.all():
            total += course.price
        print(f'Total Cost is {total}')
        return total


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1, message= 'Rating must be 1 or greater !!'),
                                                                MaxValueValidator(5, message= 'Max rating 5 is allowed !!')])
    comments = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (str(self.course), str(self.rating))







