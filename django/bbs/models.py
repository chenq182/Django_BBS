from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Client(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField('sha1 of original password', max_length=40)

    def __str__(self):
        return "Client: %s" % self.username


class User(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='related client',
    )
    name = models.CharField('nickname', max_length=20)
    email = models.EmailField(null=True)

    def __str__(self):
        return "User: %s" % self.name


class Section(models.Model):
    name = models.CharField(max_length=50)
    admins = models.ManyToManyField(User)

    def __str__(self):
        return "Section: %s" % self.name


class Forum(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    admins = models.ManyToManyField(User)

    def __str__(self):
        return "Forum: %s" % self.name

    def post_count(self):
        return self.post_set.count()

    def reply_and_post_count(self):
        return self.reply_set.count()+self.post_set.count()

    def reply_and_post_count_today(self):
        import datetime
        today = datetime.date.today()
        r = self.reply_set.filter(update__gte=today).count()
        p = self.post_set.filter(update__gte=today).count()
        return r+p

    def page_max(self):
        p = self.post_set.count()
        pages = (p-1)//20+1
        if p == 0:
            pages = 1
        return pages


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    update = models.DateTimeField("last edit's date")
    topic = models.CharField(max_length=30)
    text = models.CharField(max_length=500,blank=True,null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    top = models.IntegerField('priority', default=0)
    newdate = models.DateTimeField("last reply's date")

    def __str__(self):
        return "Post: %s [by %s]" % (self.topic, self.author.name)

    class Meta:
        ordering = ['-top', '-newdate']

    def delete(self, *args, **kwargs):
        import os
        for pfile in self.pfile_set.all():
            try:
                os.remove('/var/www/upload/'+pfile.name)
            except OSError:
                pass
        for r in self.reply_set.all():
            for rfile in r.rfile_set.all():
                try:
                    os.remove('/var/www/upload/'+rfile.name)
                except OSError:
                    pass
        super(Post, self).delete(*args, **kwargs)

    def last_reply_author(self):
        c = self.reply_set.count()
        if c==0:
            return self.author.name
        return self.reply_set.all()[c-1].author.name

    def page_max(self):
        p = self.reply_set.count()
        pages = (p-1)//20+1
        if p == 0:
            pages = 1
        return pages

    def previous(self):
        p = Post.objects.filter(newdate__gt=self.newdate).order_by('-newdate').last()
        return p

    def next(self):
        n = Post.objects.filter(newdate__lt=self.newdate).order_by('-newdate').first()
        return n

    def admin(self, username):
        if User.objects.filter(name=username).count() == 0:
            return False
        u = User.objects.get(name=username)
        if u in self.forum.admins.all():
            return True
        if u in self.forum.section.admins.all():
            return True
        return False


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    update = models.DateTimeField("last edit's date")
    text = models.CharField(max_length=500,blank=True,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    def __str__(self):
        return "Reply: %s [by %s]" % (self.text, self.author.name)

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        super(Reply, self).save(*args, **kwargs)
        self.post.newdate = self.update
        self.post.save()

    def delete(self, *args, **kwargs):
        import os
        for rfile in self.rfile_set.all():
            try:
                os.remove('/var/www/upload/'+rfile.name)
            except OSError:
                pass
        super(Reply, self).delete(*args, **kwargs)


class PFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class RFile(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


