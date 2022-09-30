from urllib import request
from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from news.models import Post
from photo.models import Photo

def HomeView(request):
    queryset1 = Post.objects.all().order_by('-modify_dt')[:4]
    queryset2 = Photo.objects.all().order_by('-upload_dt')[:4]
    context = {'posts': queryset1, 'photos':queryset2 }    
    return render(request, 'home.html', context)
    
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')
    
class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'
    
class OwnerOnlyMixin(AccessMixin):
    raise_exception = True # False로 바꾸면 로그인 페이지로 이동
    permission_denied_message = "해당 내용을 작성한 사용자만이 수정 및 삭제가 가능합니다."
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)