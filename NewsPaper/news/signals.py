from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import *


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


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        categories_type = instance.categoryType
        subscribers_email: list[str] = []

        for cat in categories:
            subscribers: list[str] = cat.subscriptions.all()
            for s in subscribers:
                subscribers_email += User.objects.filter(subscriptions=s).values_list('email', flat=True)

        print(f'{subscribers_email = }')
        if categories_type == 'nw':
            send_notifications_news(instance.preview(), instance.pk, instance.title, subscribers_email)
        else:
            send_notifications_article(instance.preview(), instance.pk, instance.title, subscribers_email)
