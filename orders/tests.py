from django.core import mail
from django.test import TestCase
from robots.models import Robot
from orders.models import Order
from customers.models import Customer

class NotifyWaitingListTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email='test@example.com')
        self.robot_serial = 'R2-D2'
        self.robot_model = 'R2'
        self.robot_version = 'D2'
        self.order = Order.objects.create(customer=self.customer, robot_serial=self.robot_serial)

    def test_notify_waiting_list(self):
        self.assertEqual(len(mail.outbox), 0)

        Robot.objects.create(
            model=self.robot_model,
            version=self.robot_version,
            serial=self.robot_serial,
            created="2022-12-31 23:05:59"
        )

        self.assertEqual(len(mail.outbox), 1)

        Robot.objects.create(
            model=self.robot_model,
            version=self.robot_version,
            serial=self.robot_serial,
            created="2022-12-31 23:06:59"
        )

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject, 'Робот в наличии!')
        self.assertEqual(mail.outbox[0].to, [self.customer.email])