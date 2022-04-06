from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import send_notification_to_subs

@receiver(m2m_changed, sender=Post.post_category.through)
def send_email_to_subs(sender, instance, action, **kwargs):

    if action == 'post_add':
        for category in instance.post_category.all():
            list_of_emails = []

            for sub in category.subscriber.all():
                list_of_emails.append(sub.email)

            category = f'{category}'
            new_post = f'{instance}'
            link = f'{instance.id}'
            send_notification_to_subs.apply_async([list_of_emails, category, new_post, link], countdown=5)
            print('Celery applied')



# @receiver(pre_save, sender=Post)
# def limit_post_handler(sender, instance, *args, **kwargs):
#     start_date = datetime.datetime.today().date()
#     end_date = start_date+datetime.timedelta(days=1)
#     posts_quantity = Post.objects.filter(author=instance.author, date_posted__range=(start_date, end_date))
    
#     if len(posts_quantity) > 3:
#         redirect('/news/')
