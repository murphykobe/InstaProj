from annoying.decorators import ajax_request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.models import Post,InstaUser,UserConnection,Comment,Like
from Insta.forms import CustomUserCreationForm

# Create your views here.

class PostView(LoginRequiredMixin,ListView):
    model=Post
    template_name='index.html'
    login_url='login'

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        try:
            for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
                following.add(conn.following)
            return Post.objects.filter(author__in=following).order_by('-posted_on')
        except:
            return Post.objects.filter().order_by('-posted_on')

class PostDetail(LoginRequiredMixin,DetailView):
    model=Post
    template_name='post_details.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked']=1
        else:
            data['liked']=0
        return data

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'
    
    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]

class CreatePost(CreateView):
    model=Post
    template_name='create_post.html'
    fields = ('title','image',)

    def form_valid(self, form):
        current_user = InstaUser.objects.get(pk=self.request.user.pk)
        author=current_user
        form.instance.author = author
        return super(CreatePost, self).form_valid(form)

class UpdatePost(UpdateView):
    model=Post
    template_name='update_post.html'
    fields = ('title',)

class DeletePost(DeleteView):
    model=Post
    template_name='delete_post.html'
    success_url = reverse_lazy('home')

class UserSignUp(CreateView):
    form_class=CustomUserCreationForm
    template_name='registration/sign_up.html'
    success_url = reverse_lazy('login')

class UserDetail(DetailView):
    model=InstaUser
    template_name='user_profile.html'

class EditUser(UpdateView):
    model=InstaUser
    template_name='edit_profile.html'
    fields=['profile_pic','username']
    login_url='login'

class FollowerView(ListView):
    model=InstaUser
    template_name='follower_view.html'

    def get_queryset(self, **kwargs):
        current_user = InstaUser.objects.get(pk=self.kwargs.get('pk'))
        follower = set()
        try:
            for conn in UserConnection.objects.filter(following=current_user).select_related('creator'):
                follower.add(conn.creator.pk)
            return InstaUser.objects.filter(pk__in=follower)
        except:
            return InstaUser.objects.filter()

class FollowingView(ListView):
    model=InstaUser
    template_name='following_view.html'

    def get_queryset(self,**kwargs):
        current_user = InstaUser.objects.get(pk=self.kwargs.get('pk'))
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('creator'):
            following.add(conn.following.pk)
        return InstaUser.objects.filter(pk__in=following)


@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }