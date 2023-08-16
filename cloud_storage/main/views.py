from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import View
from .forms import UploadForm, SignUpForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
import os
import sys
import subprocess
import codecs
from django.contrib.auth.decorators import login_required # defで記載するものの規制用
from django.contrib.auth.mixins import LoginRequiredMixin # classで記載するものの規制用
from django.db.models import Q
from functools import reduce
from operator import and_
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
import time
import shutil
from django.http import FileResponse
from PIL import Image
import cv2


media_dir = r"F:\DATE\server_media\cloud_media/"

# Create your views here.
class Index(LoginRequiredMixin,generic.ListView):

    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

    context_object_name = 'post_list'
    queryset = Post.objects.order_by('-file_name')


    #paginate_by = 15

    def get_queryset(self):
        queryset = Post.objects.order_by('-id')
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
            Q(file_name__icontains=query)
            )

        #c_num = queryset.count()#検索結果の値が入ってるよ
        #params = {'c_num' : str(c_num)}

        return queryset

# DetailViewは詳細を簡単に作るためのView
class Detail(LoginRequiredMixin,DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post



class Create(LoginRequiredMixin,CreateView):
    template_name = "main/post_form.html"
    model = Post
    form_class = UploadForm
    #success_url = reverse_lazy('/')
    def post(self, request):
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                for ff in request.FILES.getlist('file_name'):
                    re_user_name = request.user.username
                    p = Post(file_name=ff,user_name=re_user_name)
                    p.save()

                    upload_file_name = ff.name
                    upload_file_name = upload_file_name.replace(" ","_")
                    upload_file_name = upload_file_name.replace("(","")
                    upload_file_name = upload_file_name.replace(")","")

                    account_dir = str(media_dir) + str(re_user_name) + '/'
                    if os.path.isdir(account_dir) == False :
                        os.mkdir(str(media_dir) + str(re_user_name))

                    root, ext = os.path.splitext(str(upload_file_name))
                    ext = ext.replace('.','')

                    if str(ext) == 'jpg' or str(ext) == 'jpeg' or str(ext) == 'png' or str(ext) == 'webp' :
                        try:
                            bairitsu = 8 #倍率指定
                            imagedata = Image.open(str(media_dir) + str(upload_file_name))
                            width, height = imagedata.size
                            width2 = width/bairitsu
                            height2 = height/bairitsu
                            imagedata2= imagedata.resize((int(width2),int(height2)))
                            newimage = str(media_dir) + 'low_' + str(upload_file_name)
                            imagedata2.save(newimage, quality=85,optimize=True)
                            del imagedata
                            del imagedata2
                        except Exception as e:
                            print(e)



                    try:
                        shutil.copy(str(media_dir) + str(upload_file_name), str(account_dir) + str(upload_file_name))
                        os.remove(str(media_dir) + str(upload_file_name))
                        if str(ext) == 'jpg' or str(ext) == 'jpeg' or str(ext) == 'png' or str(ext) == 'webp' :
                            shutil.copy(str(media_dir) + 'low_' + str(upload_file_name), str(account_dir) + 'low_' + str(upload_file_name))
                            os.remove(str(media_dir) + 'low_' + str(upload_file_name))

                    except Exception as e:
                        print(e)

            return HttpResponseRedirect('/TCloud/')

        return render(request, 'TCloud/post_form.html', {'form': form})

    success_url = '/TCloud/'


class Delete(LoginRequiredMixin,DeleteView):
    model = Post
    # 削除したあとに移動する先（トップページ）
    success_url = "/TCloud/"

    def post(self, request,**kwargs):
        try:
            date = Post.objects.get(id=int(kwargs['pk']))
            file_name_re = date.file_name
            re_user_name = request.user.username
            date.delete()
            os.remove(str(media_dir) + str(re_user_name) + '/' + str(file_name_re))

            root, ext = os.path.splitext(str(file_name_re))
            ext = ext.replace('.','')

            if str(ext) == 'jpg' or str(ext) == 'jpeg' or str(ext) == 'png' or str(ext) == 'webp' :
                os.remove(str(media_dir) + str(re_user_name) + '/' + 'low_' + str(file_name_re))

        except :
            pass
        return HttpResponseRedirect('/TCloud/')

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            post = post_data.filter(
                     Q(title__icontains=keyword)
                   )
            #messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'main/post_list.html', {'post': post })
