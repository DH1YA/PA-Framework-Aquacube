from django.db import models

class Users(models.Model):
    CUSTOMER = 1
    AGENT = 2
    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (AGENT, 'Agent'),
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) # Panjang standar untuk password hash di Django
    role = models.IntegerField(choices=ROLE_CHOICES) # 1 = Customer, 2 = Agent

    def save(self, *args, **kwargs):
        super(Users, self).save(*args, **kwargs)
        if not self.username.startswith(str(self.id)):
            self.username = f'{self.id}_{self.username}'
            super(Users, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
