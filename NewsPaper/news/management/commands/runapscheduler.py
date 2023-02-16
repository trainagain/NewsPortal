import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Subscriber, Post, User

logger = logging.getLogger(__name__)


def my_job():
    pass
    # today = datetime.datetime.now()
    # last_week = today - datetime.timedelta(days=7)
    # posts = Post.objects.filter(dateCreation__gte=last_week)
    # categories = set(posts.values_list('postCategory__id', flat=True))
    # subscriptions = []
    # for cat in categories:
    #     subscribers = Subscriber.objects.filter(category=cat).values_list('user', flat=True)
    #     for s in subscribers:
    #         subscriptions += User.objects.filter(id=s).values_list('email', flat=True)
    #
    # html_content = render_to_string('daily_post.html',
    #                                 {
    #                                     'link': settings.SITE_URL,
    #                                     'posts': posts,
    #                                 }
    #                                 )
    #
    # msg = EmailMultiAlternatives(subject='Статьи за неделю.', body='',
    #                              from_email=settings.DEFAULT_FROM_EMAIL,
    #                              to=subscriptions)
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()
    #


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour="18", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")