from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime, timedelta
from .models import *


@shared_task
def send_notifications_news(preview, pk, title, subscriptions):
    html_content = render_to_string('post_created_email.html',
                                    {
                                       'text': preview,
                                       'link': f'{settings.SITE_URL}/news/{pk}',
                                       'title': title
                                    }
                                    )

    msg = EmailMultiAlternatives(subject=title, body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscriptions)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_notifications_article(preview, pk, title, subscriptions):
    html_content = render_to_string('post_created_email.html',
                                    {
                                       'text': preview,
                                       'link': f'{settings.SITE_URL}/article/{pk}',
                                       'title': title
                                    }
                                    )

    msg = EmailMultiAlternatives(subject=title, body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscriptions)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def my_job():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__id', flat=True))
    subscriptions = []
    for cat in categories:
        subscribers = Subscriber.objects.filter(category=cat).values_list('user', flat=True)
        for s in subscribers:
            subscriptions += User.objects.filter(id=s).values_list('email', flat=True)

    html_content = render_to_string('daily_post.html',
                                    {
                                        'link': settings.SITE_URL,
                                        'posts': posts,
                                    }
                                    )

    msg = EmailMultiAlternatives(subject='Статьи за неделю.', body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscriptions)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
