from django import forms
from myapp.models import Order, Review, Student

class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8,'8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks')
    ]
    name = forms.CharField(label='Student Name',max_length=100,required=False)
    length = forms.TypedChoiceField(required=False,label='Preferred course duration:',
                                    widget=forms.RadioSelect,choices=LENGTH_CHOICES,coerce=int)
    max_price = forms.IntegerField(required=True,label='Maximum Price',min_value=0)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses','Student','order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(),
                   'order_type': forms.RadioSelect}
        labels = {'Student': u'Student Name',}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer','course','rating','comments']
        widgets = {'course': forms.RadioSelect}
        labels = {'reviewer': 'Please enter a valid email!',
                  'rating': 'Rating: An integer between 1(worst) and 5(best)'}

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username','password','email','first_name','last_name','interested_in']
        widgets = {'interested_in': forms.CheckboxSelectMultiple, 'password': forms.PasswordInput}
        labels = {'interested_in': 'Select the topics that you are interested in'}

class ForgotPasswordForm(forms.Form):
    Email = forms.EmailField()

    def __str__(self):
        return self.Email




