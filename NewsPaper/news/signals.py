from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .task import *


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
            send_notifications_news.delay(instance.preview(), instance.pk, instance.title, subscribers_email)
        else:
            send_notifications_article.delay(instance.preview(), instance.pk, instance.title, subscribers_email)
