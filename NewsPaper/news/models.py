from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating') if postRat.get('postRating') else 0

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating') if commentRat.get('commentRating')else 0

        for post in self.post_set.all():
            comPosRat = post.comment_set.aggregate(CommentPostRating=Sum('rating'))
        cpRat = 0
        cpRat += comPosRat.get('CommentPostRating') if comPosRat.get('CommentPostRating') else 0

        self.ratingAuthor = pRat * 3 + cRat + cpRat
        self.save()

    def __str__(self):
        return '{}'.format(self.authorUser)


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'nw'
    ARTICLE = 'ar'
    CATEGORY_CHOICES = ((NEWS, 'Новость'), (ARTICLE, 'Статья'))
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return '{}...'.format(self.text[0:19])


    def __str__(self):
       return '{}'.format(self.title)
    


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return '{}'.format(self.commentPost)
