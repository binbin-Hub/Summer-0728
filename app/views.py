from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django. http import HttpResponseRedirect
from django.db.models import Q

from django. urls import reverse_lazy
from . models import Blog

class index(ListView):
    template_name = 'index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        return Blog.objects.all
        
class detail(DetailView):
    model = Blog
    template_name = 'detail.html'
    context_object_name = 'blog'
# 객체 이름을 blog 라고 썼기 때문에 detail.html 에서 blog 라는 이름을 사용할 수 있음
# ListView : model 을 연결시키고 list를 다 불러 오겠다!, 불러온 정보를 blog_list 라고 부르겠다 ! 

class delete(DeleteView):
    model = Blog
    template_name = 'delete.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('index')

class update(UpdateView):
    model = Blog
    template_name = 'update.html'
    fields = ['title', 'text']
    success_url = reverse_lazy('index')

class create(CreateView):
    model = Blog
    template_name = 'create.html'
    fields = ['title', 'text']

def form_valid(self, form):
    Blog = form.save(commit=False)
    Blog.author = self.request.user
    Blog.save()

    return HttpResponseRedirect(self.request.POST.get('next', '/'))

def result(request):
    BlogPosts = Blog.objects.all()

    query = request.GET.get('query', '')

    if query:
        BlogPosts = BlogPosts.filter(Q(title__icontains=query)| Q(text__icontains=query)).order_by('-time')

    return render(request, 'result.html', {'BlogPosts':BlogPosts, 'query' : query})

    #icontains-> 검색한 키워드가 안에 담겨있으면 결과값을 모두 가져옴
    