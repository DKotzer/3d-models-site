
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Comment, Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic import  DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, path
from .forms import AccountCreate,EditProfileForm, EditUserForm
from django.urls import reverse, path
from .forms import AccountCreate
from .forms import EditProfileForm
import uuid
import boto3
import os
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage




# Add these "constant" variables below the imports
S3_BASE_URL = os.getenv('S3_BASE_URL')
S3_LINK_URL = os.getenv('S3_LINK_URL')
BUCKET = os.getenv('BUCKET')


#add photo function mostly from the lesson markdown
@login_required
def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_LINK_URL}{key}"
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('photo An error occurred uploading file to S3')
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))


#home page view with pagination and sorted by newest first
def home(request):
    post_list = Post.objects.all()
    for post in post_list: 
        post.like_count = len(post.likes.all())
    new_sort = sorted(post_list, key=attrgetter('pk'), reverse=True)
    #infiniscroll test
    page = request.GET.get('page', 1)
    paginator = Paginator(new_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list , 'posts': posts})

#home page view with pagination and sorted by oldest first
def home_oldest(request):
    post_list = Post.objects.all()
    for post in post_list: 
        post.like_count = len(post.likes.all())
    old_sort = sorted(post_list, key=attrgetter('pk'), reverse=False)
    #infiniscroll test
    page = request.GET.get('page', 1)
    paginator = Paginator(old_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list , 'posts': posts})

#home page view with pagination and sorted by most likes
def home_likes(request):
    post_list = Post.objects.all()
    for post in post_list: 
        post.like_count = len(post.likes.all())
    like_sort = sorted(post_list, key=attrgetter('like_count'), reverse=True)
    #infiniscroll test
    page = request.GET.get('page', 1)
    paginator = Paginator(like_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list , 'posts': posts})

#post index page view with pagination and sorted by newest first
def posts_index(request):
    post_list = Post.objects.all()
    for post in post_list: 
        post.like_count = len(post.likes.all())
    new_sort = sorted(post_list, key=attrgetter('pk'), reverse=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(new_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'main_app/posts_index.html', {'post_list': post_list , 'posts': posts})

#post index page view with pagination and sorted by most likes
def posts_index_likes(request):
    post_list = Post.objects.all()
    for post in post_list: 
        post.like_count = len(post.likes.all())

    like_sort = sorted(post_list, key=attrgetter('like_count'), reverse=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(like_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'main_app/posts_index.html', {'post_list': post_list , 'posts': posts})

#post index page view with pagination and sorted by oldest first
def posts_index_oldest(request):
    post_list = Post.objects.all()
    for post in post_list: 
        post.like_count = len(post.likes.all())

    
    old_sort = sorted(post_list, key=attrgetter('pk'), reverse=False) 
    
    page = request.GET.get('page', 1)
    paginator = Paginator(old_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'main_app/posts_index.html', {'post_list': post_list , 'posts': posts})

#view of users posts with pagination
@login_required
def user_posts_index(request):
    post_list = Post.objects.filter(user=request.user.id)
    for post in post_list: 
        post.like_count = len(post.likes.all())
    #infiniscroll test
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'main_app/user_posts_index.html', {'post_list': post_list , 'posts': posts})


#signup automatically creates an account adds the account picture to it via form and then saves the user and account with default picture if none is uploaded
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        
        account_pic = request.FILES.get('picture', None)
        
        print("photo file test",account_pic)
        if account_pic:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + account_pic.name[account_pic.name.rfind('.'):]
            print("key test", key)
            s3.upload_fileobj(account_pic, BUCKET, key)
            # build the full url string
            url = f"{S3_LINK_URL}{key}"
            print('url',url)
            account_form = AccountCreate(request.POST)
            if form.is_valid():
                print("accountForm", account_form)
                #save user to DB
                user = form.save()
                account = account_form.save(commit=False)
                account.user = user
                account.picture = url
                print('AccountURL:', account.picture)
                account.save()
                #login the user
                login(request, user)
                return redirect('/')
            else:
                error_message = "Invalid Sign Up Submission - Try Again"
        else:    
            account_form = AccountCreate(request.POST)
            if form.is_valid():
                print("accountForm", account_form)
                user = form.save()
                account = account_form.save(commit=False)
                account.user = user
                account.picture = "/media/models/accountImg/default.png"
                print('AccountURL:', account.picture)
                account.save()
                login(request, user)
                return redirect('/')
        
    form = EditUserForm()
    account_form = AccountCreate()
    context = {'form':form, 'error_message': error_message , 'account_form': account_form}
    return render(request, 'registration/signup.html', context)


#Profile detail CBV that is probably unused
class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Account

#the actual profile view that we are using, counts total likes and shows the posts you have liked in a list sorted by newest first
@login_required
def profile(request):
    profile_details = Account.objects.all()
    like_count = 0
    holder = request.user
    posts = Post.objects.filter(user=holder.id)
    post_count =  len(posts)
    for post in posts:
        like_count += (post.likes.all().count())
        
    post_sort = Post.objects.filter(likes=request.user.id)
    print(post_sort)
    new_sort = sorted(post_sort, key=attrgetter('pk'), reverse=True)
   
    page = request.GET.get('page', 1)
    paginator = Paginator(new_sort, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'registration/profile.html', {'profile_details':profile_details, 'like_count':like_count, 'post_count':post_count, 'posts': posts})


@login_required
def add_model(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('model', None)
    print("photo file test",photo_file)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_LINK_URL}{key}"
            photo = Photo(url=url, post_id=post_id)
            post = Post.objects.get(id=post_id)
            post.model = photo.url
            post.save()
        except:
            print('An error occurred uploading file to S3')
        
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    # fields = '__all__'
    fields = ['title','model','text_content','tags','type']
    success_url = '/main_app/templates/home.html'
    
    #overriding in child class
    def form_valid(self, form, *args,**kwargs, ):
        print("POST Test",self.request.POST)
        form = Post(title=self.request.POST.get('title'),text_content=self.request.POST.get('text_content'),tags=self.request.POST.get('tags') )
        form.user_id = self.request.user.id
        form.save()
        add_model(self.request, form.id)
        post = Post.objects.get(id=form.id)
        print("post test",post.title)
        return HttpResponseRedirect(reverse('post_detail', args=[form.id]))
         

#Class based Update View
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','text_content','tags','type']
    
#Class based delete view
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"   
    
    

#the model details page, checks if person viewing has like already. 
@login_required
def detail(request, pk):
    post = Post.objects.get(id=pk)
    own_post = False
    if post.user == request.user:
        own_post = True
    if request.user in Post.objects.get(id=pk).likes.all():
        liked = True
    else:
        liked = False
    print(Post.objects.get(id=pk).likes.all())
    return render(request,'main_app/post_detail.html',{'post': post, 'liked': liked, 'own_post': own_post})

    
#class based comment create view with some fancyness to get access to the post id that only took 2 days to figure out.
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    # fields = '__all__'
    fields = ['title','text_content']
    
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        print("initial test",initial)
        return initial
    
    def form_valid(self, form, *args,**kwargs, ):
        # print("POST Test",self.request.POST)
        form = Comment(title=self.request.POST.get('title'),text_content=self.request.POST.get('text_content'))
        form.user_id = self.request.user.id
        form.post_id = self.kwargs.get('pk')
        form.save()
        # comment = Comment.objects.get(id=form.id)
        return HttpResponseRedirect(reverse('post_detail', args=[form.post_id]))
    
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['title','text_content']
    
class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
    )


    def get_success_url(self):
        print('self',self.request)
        return self.request.GET.get('next', reverse('posts_index')) 
    

@login_required
def LikeView(request, pk):
    print("POST", Post)
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

@login_required
def UnlikeView(request, pk):
    print("POST", Post)
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print('before',post.likes)
    post.likes.remove(request.user)
    print('after', post.likes)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def SearchPost(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(Q(tags__icontains=searched)| Q(title__icontains=searched))
        return render(request, 'main_app/post_search.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'main_app/post_search.html', {})

class UserEditView(generic.CreateView):
    form_class = EditProfileForm
    template = 'registration/edit_profile.html'
    success_url = '/home' 


@login_required
def edit_profile(request):
    error_message = ''
    if request.method == 'POST':
        form = EditUserForm(data=request.POST, instance=request.user)
        account_instance = get_object_or_404(Account, user=request.user)
        
        account_pic = request.FILES.get('picture', None)
        print("photo file test",account_pic)
        if account_pic:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + account_pic.name[account_pic.name.rfind('.'):]
            print("key test", key)
            # just in case something goes wrong
            try:
                s3.upload_fileobj(account_pic, BUCKET, key)
                # build the full url string
                url = f"{S3_LINK_URL}{key}"
                print('url',url)
                account_instance.picture = url
                
                account_form = AccountCreate(request.POST or None, request.FILES or None, instance=account_instance)
                if form.is_valid():
                    print("accountForm", account_form)
                    #save user to DB
                    user = form.save()
                    account = account_form.save(commit=False)
                    print("I AM HERE")
                    # account_form.save()
                    # account = account_form.save()
                    print("ACCOUNT", account.picture)
                    account.user = user
                    account.picture = url
                    account.save()
                    print("HELLO",account.picture)
                    login(request, user)
                    
                    return redirect('/')
                
                else:
                    error_message = "Invalid Edit Submission - Try Again"
                        
            except:
                
                print('An error occurred uploading file to S3')
    form = EditUserForm(instance=request.user)
    account_form = AccountCreate(instance=request.user)
    context = {'form':form, 'error_message': error_message, 'account_form': account_form}
    return render(request, 'registration/edit_profile.html', context)

