from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):

        rating = self.post_set.all().aggregate(postRating=Sum('post_rating'))
        post_rating = 0
        post_rating += rating.get('postRating')
        rating = self.user.comment_set.all().aggregate(commentRating=Sum('comment_rating'))
        comment_rating = 0
        comment_rating += rating.get('commentRating')

        self.author_rating = post_rating * 3 + comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')

    ARTICLE = 'AR'
    NEWS = 'NE'

    POST_TYPE_CHOICES = [
        (ARTICLE, 'Article'),
        (NEWS, 'News')
    ]

    post_type = models.CharField(
        max_length=2,
        choices=POST_TYPE_CHOICES,
        default=ARTICLE
    )

    date_posted = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        preview = self.text[:124]
        return f'{preview}...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text_comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return self.text_comment
