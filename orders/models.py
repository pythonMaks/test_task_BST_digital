from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from robots.models import Robot
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)


@receiver(post_save, sender=Robot)
def notify_waiting_list(sender, instance, created, **kwargs):
    if created:
        waiting_list = Order.objects.filter(robot_serial=instance.serial)
        for entry in waiting_list:
            if not Robot.objects.filter(serial=instance.serial).exclude(id=instance.id).exists():
                send_mail(
                    'Робот в наличии!',
                    f'Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n'
                    'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.',
                    'test_task_bst@rambler.ru',
                    [entry.customer.email],
                )
