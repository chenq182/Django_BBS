# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render, redirect, get_object_or_404
import hashlib, string

from .models import Client, User, Section, Forum, Post, Reply, PFile


def index(request):
    return render(request, 'bbs/index.html', {'sections': Section.objects})


def forum(request, forum_id="0", page="1"):
    f = get_object_or_404(Forum, pk=string.atoi(forum_id))
    p = string.atoi(page)
    return render(request, 'bbs/forum.html', {
        'forum': f, 'page': p, 'posts': f.post_set.all()[(p-1)*20:p*20]
        })


from .forms import New_PostForm
def new_post(request, forum_id="0"):
    if not request.session.has_key('bbsname'):
        return redirect('bbs:login')
    f = get_object_or_404(Forum, pk=string.atoi(forum_id))
    if request.method == 'POST':
        form = New_PostForm(request.POST, request.FILES)
        if form.is_valid():
            to = form.cleaned_data['topic']
            te = form.cleaned_data['text']
            u = get_object_or_404(User, name=request.session['bbsname'])
            import datetime
            n = datetime.datetime.now()
            p = Post(author=u, date=n, update=n, topic=to, text=te, forum=f, newdate=n)
            p.save()
            files = request.FILES.getlist('files')
            for fi in files:
                filename = 'p'+str(p.id)+'-'+fi.name
                with open('/var/www/upload/'+filename, 'wb+') as destination:
                    for chunk in fi.chunks():
                        destination.write(chunk)
                pfile = PFile(post=p, name=filename)
                pfile.save()
            return redirect('bbs:post', p.id, 1)
    else:
        form = New_PostForm()
    return render(request, 'bbs/new_post.html', {'forum': f, 'form': form})


from .forms import ReplyForm
def post(request, post_id="0", page="1"):
    po = get_object_or_404(Post, pk=string.atoi(post_id))
    pa = string.atoi(page)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data['text']
            u = get_object_or_404(User, name=request.session['bbsname'])
            import datetime
            n = datetime.datetime.now()
            r = Reply(author=u, date=n, update=n, text=t, post=po, forum=po.forum)
            r.save()
            return redirect('bbs:post', po.id, po.page_max())
    else:
        form = ReplyForm()
    admin = False
    if request.session.has_key('bbsname'):
        if po.admin(request.session['bbsname']):
            admin = True
    return render(request, 'bbs/post.html', {
        'post': po, 'page': pa, 'form': form, 'floor': (pa-1)*20+1,
        'admin': admin,
        'replies': po.reply_set.all()[(pa-1)*20:pa*20]
        })


def del_post(request, post_id="0"):
    p = get_object_or_404(Post, pk=string.atoi(post_id))

    if not request.session.has_key('bbsname'):
        return redirect('bbs:login')
    u = get_object_or_404(User, name=request.session['bbsname'])
    if u!=p.author and not p.admin(request.session['bbsname']):
        context = {'message': '无权限进行此操作！'}
        return render(request, 'bbs/system_message.html', context)

    p.delete()
    return redirect('bbs:forum', p.forum.id, 1)


def del_reply(request, reply_id="0"):
    r = get_object_or_404(Reply, pk=string.atoi(reply_id))

    if not request.session.has_key('bbsname'):
        return redirect('bbs:login')
    u = get_object_or_404(User, name=request.session['bbsname'])
    if u!=r.author and not r.post.admin(request.session['bbsname']):
        context = {'message': '无权限进行此操作！'}
        return render(request, 'bbs/system_message.html', context)

    r.delete()
    return redirect('bbs:post', r.post.id, 1)


def top_post(request, post_id="0", top="0"):
    p = get_object_or_404(Post, pk=string.atoi(post_id))

    if not request.session.has_key('bbsname'):
        return redirect('bbs:login')
    if not p.admin(request.session['bbsname']):
        context = {'message': '无权限进行此操作！'}
        return render(request, 'bbs/system_message.html', context)

    p.top = string.atoi(top)
    p.save()
    return redirect('bbs:forum', p.forum.id, 1)


def login(request):
    if request.session.has_key('bbsname'):
        context = {'message': request.session['bbsname'] +
            ': 您已登录！'}
        return render(request, 'bbs/system_message.html', context)
    e = ''
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        from django.core.exceptions import ObjectDoesNotExist
        try:
            c = Client.objects.get(username=u)
            if c.password == hashlib.sha1(p).hexdigest():
                request.session.flush()
                request.session['bbsname'] = c.user.name
                return render(request, 'bbs/index.html', {'sections': Section.objects})
            e += '密码错误！'
        except ObjectDoesNotExist:
            e += '用户不存在！'
    return render(request, 'bbs/login.html', {'error_message': e})


def logout(request):
    try:
        del request.session['bbsname']
    except KeyError:
        pass
    request.session.flush()
    return render(request, 'bbs/index.html', {'sections': Section.objects})


from .forms import RegisterForm
def register(request):
    if request.session.has_key('bbsname'):
        context = {'message': request.session['bbsname'] +
            ': 您已登录！'}
        return render(request, 'bbs/system_message.html', context)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            n = form.cleaned_data['nickname']
            c = Client(username=u, password=hashlib.sha1(p).hexdigest())
            c.save()
            User.objects.create(client=c, name=n)
            request.session.flush()
            request.session['bbsname'] = n
            return render(request, 'bbs/index.html', {'sections': Section.objects})
    else:
        form = RegisterForm()
    return render(request, 'bbs/register.html', {'form': form})


def user(request):
    pass


