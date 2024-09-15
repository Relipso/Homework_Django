from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version, Category
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from .services import get_categories


class ModeratorProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/moderator_product_update.html'
    success_url = reverse_lazy('catalog:products_list')
    permission_required = ('catalog.can_change_product_description', 'catalog.can_change_product_category')

    def form_valid(self, form):
        if self.request.user.has_perm('catalog.can_change_product_description'):
            form.instance.description = form.cleaned_data['description']
        if self.request.user.has_perm('catalog.can_change_product_category'):
            form.instance.category = form.cleaned_data['category']
        return super().form_valid(form)


@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:products_list')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        for product in context_data['product_list']:
            active_version = Version.objects.filter(product=product, version_sign=True)
            if active_version:
                product.active_version = active_version.last().version_name
            else:
                product.active_version = 'Отсутствует'

            product.can_unpublish = self.request.user.has_perm('catalog.can_unpublish_product')
            product.can_edit_as_moderator = self.request.user.has_perm('catalog.can_change_product_description') or \
                                            self.request.user.has_perm('catalog.can_change_product_category')
        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user == self.get_object().owner or
                request.user.has_perm('catalog.can_change_product_description') or
                request.user.has_perm('catalog.can_change_product_category')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user == self.object.owner:
            # Владелец может изменять все поля
            return super().form_valid(form)
        else:
            # Модератор может изменять только определенные поля
            if self.request.user.has_perm('catalog.can_change_product_description'):
                self.object.description = form.cleaned_data['description']
            if self.request.user.has_perm('catalog.can_change_product_category'):
                self.object.category = form.cleaned_data['category']
            self.object.save()
            return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user == self.object.owner:
            ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
            if self.request.method == 'POST':
                context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
            else:
                context_data['formset'] = ProductFormset(instance=self.object)
        return context_data


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')


class BasePageView(TemplateView):
    template_name = "catalog/base.html"


class ContactsPageView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")

            print(
                f"{name} написал следующее сообщение: {message}, контактный телефон: {phone}"
            )
        return render(request, "catalog/contacts.html")


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_categories()
