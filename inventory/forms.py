from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Inventory, Category

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class InventoryForm(forms.ModelForm):
    
    category_items = Category.objects.all()
    category = forms.ModelChoiceField(queryset=category_items, initial=0)
    
    class Meta:
        model = Inventory
        fields = ['name', 'quantity', 'category']