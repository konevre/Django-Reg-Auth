from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from .models import Post, Author
from django.core.mail import send_mail
import datetime
from django.utils import timezone
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=Post.post_category.through)
def send_email_to_subs(sender, instance, action, **kwargs):

    if action == 'post_add':
        list_of_subs = []
        for category in instance.post_category.all():
            for sub in category.subscriber.all():
                list_of_subs.append(sub)

        for user in list_of_subs:

            html_content = render_to_string(
                'new_post_mail.html',
                {'category': category, 'post': instance, }
            )

            message = EmailMultiAlternatives(
                subject=f'New post in {category.category_name}!',
                body=f'New post',
                from_email='****@yandex.ru',
                to=[user.email, ],
                )

            message.attach_alternative(html_content, "text/html")
            message.send()

            # send_mail(
            #     subject=f'New post!',
            #     message=f'{instance.title}...',
            #     from_email='romamaster@yandex.ru',
            #     recipient_list=[user.email, ],
            # )


# @receiver(pre_save, sender=Post)
# def limit_post_handler(sender, instance, *args, **kwargs):
#     start_date = datetime.datetime.today().date()
#     end_date = start_date+datetime.timedelta(days=1)
#     posts_quantity = Post.objects.filter(author=instance.author, date_posted__range=(start_date, end_date))
    
#     if len(posts_quantity) > 3:
#         redirect('/news/')
