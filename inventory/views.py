from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from .models import Inventory, Category
from .forms import InventoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages 


class Index(TemplateView):
    template_name = 'inventory/index.html'


class SignUpView(View):
    
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
                
            login(request, user)
            return redirect('index')
        
        return render(request, 'inventory/signup.html', {'form': form})
   
    
class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        user = self.request.user.id
        items = Inventory.objects.filter(user=user).order_by('id')
        
        low_quantity = Inventory.objects.filter(
                user=user,
                quantity__lte=LOW_QUANTITY
            )
        
        if low_quantity.count() != 0:
            messages.error(request, f'{low_quantity.count()} items have low quantity' )
        
        low_quantity_ids = low_quantity.values_list('id', flat=True)

        context ={
            'items':items,
            'low_quantity_ids':low_quantity_ids
        }
                
        return render(request, 'inventory/dashboard.html', context)
    
    
class AddItem(LoginRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    model =  Inventory
    form_class = InventoryForm
    template_name ='inventory/item_form.html' 
    success_url = reverse_lazy('dashboard')
    
    
class DeleteItem(LoginRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'