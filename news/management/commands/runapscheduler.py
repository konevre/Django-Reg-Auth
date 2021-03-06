import logging

from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from news.models import Category, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
 
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    print('Sending weekly newsletter...')
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    weekday = datetime.datetime.isoweekday(datetime.datetime.now())

    if weekday == 7:
        for category in Category.objects.all():
            for sub in category.subscriber.all():
                list_of_subs = []
                list_of_subs.append(sub)

                all_posts = Post.objects.filter(
                    post_category__category_name=category,
                    date_posted__range=(last_week, today)
                    )
                for user in list_of_subs:

                    html_content = render_to_string(
                        'weekly_mail.html',
                        {'category': category, 'all_posts': all_posts, }
                    )
                    message = EmailMultiAlternatives(
                        subject='All posts for a week',
                        body=f'Weekly posts mailing',
                        from_email='romamaster@yandex.ru',
                        to=[user.email, ],
                        )

                    message.attach_alternative(html_content, "text/html")
                    message.send()


 
 
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="sun", hour="12", minute="00"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")