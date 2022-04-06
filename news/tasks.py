from .models import Category, Post
import datetime
import time
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_notification_to_subs(list_of_emails, category, new_post, link):

    html_content = render_to_string(
        'new_post_mail.html',
        {'category': category, 'post': new_post, 'link': link}
    )

    message = EmailMultiAlternatives(
        subject=f'New post in your subscribtions!',
        body=f'New post',
        from_email='romamaster@yandex.ru',
        to=list_of_emails,
        )

    message.attach_alternative(html_content, "text/html")
    message.send()
    print(f'Emails sent to {list_of_emails}.')


@shared_task
def send_newsletter():

    if datetime.datetime.isoweekday(datetime.datetime.now()) == 1:
        print('Sending weekly newsletter...')
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        for category in Category.objects.all():
            for sub in category.subscriber.all():
                list_of_subs = []
                list_of_subs.append(sub)

                for user in list_of_subs:

                    all_posts = Post.objects.filter(
                        post_category__category_name=category,
                        date_posted__range=(last_week, today)
                        )

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
                    print(f'Weekly newsletter to {list_of_subs} is sent!')

    