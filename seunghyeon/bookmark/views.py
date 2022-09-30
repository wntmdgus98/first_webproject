from django.views.generic import *
from bookmark.models import Bookmark # [주의]
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from miniproject.views import OwnerOnlyMixin

# Create your views here.
class BookmarkLV(ListView):
    model = Bookmark
    
class BookmarkDV(DetailView):
    model = Bookmark
    
#LoginRequiredMixin -> 로그인한 사용자가 아니면 로그인 페이지로 이동
class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model=Bookmark
    fields=['title','url']
    success_url=reverse_lazy('bookmark:index')
    
    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super().form_valid(form)
    
# object_list -> 현재 로그인한 사용자가 작성한 Bookmark
class BookmarkChangeLV(LoginRequiredMixin, ListView):
    template_name='bookmark/bookmark_change_list.html'
    
    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)
    
# OwnerOnlyMixin -> 작성만이 수정할 수 있도록
class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):
    model=Bookmark
    fields=['title','url']
    success_url=reverse_lazy('bookmark:index')
    
# OwnerOnlyMixin -> 작성만이 삭제할 수 있도록
class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):
    model=Bookmark
    success_url=reverse_lazy('bookmark:index')