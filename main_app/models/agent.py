from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

class agent(models.Model):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    company_phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    photo = models.ImageField(upload_to='company_picture/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.pk:  # Hanya hash untuk instance baru
            self.password = make_password(self.password)
        super(agent, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(post_save, sender=agent)
def create_user_for_agent(sender, instance, created, **kwargs):
    if instance.is_verified and not User.objects.filter(email=instance.email).exists():
        # Membuat User yang sesuai menggunakan password yang sudah di-hash
        user = User.objects.create_user(
            username=instance.company_name, 
            email=instance.email,
            password=instance.password  # Gunakan password yang sudah di-hash
        )

        # Menambahkan user ke grup 'Agent'
        agent_group, _ = Group.objects.get_or_create(name='Agent')
        user.groups.add(agent_group)