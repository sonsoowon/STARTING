
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
class ServiceUserManager(BaseUserManager):
    def create_user(self, id, email, name, phone, department, gender=None, birth=None, password=None):
        if not (id and email and name and phone and department):
            raise ValueError("Users must have id, email, name, phone, department information")
        
        user = self.model(
            id = id,
            email = self.normalize_email(email),
            name = name,
            phone = phone,
            department = department,
            gender = gender,
            birth = birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, name, phone, department, gender=None, birth=None, password=None):
        if not (id and email and name and phone and department):
            raise ValueError("Users must have id, email, name, phone, department information")
        
        user = self.model(
            id = id,
            email = self.normalize_email(email),
            password = password,
            name = name,
            phone = phone,
            department = department,
            gender = gender,
            birth = birth
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class ServiceUser(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField()
    phone = models.CharField(max_length=11)
    department = models.CharField()
    gender = models.CharField(blank=True)
    birth = models.DateField(blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ServiceUserManager()

    USERNAME_FIELD = 'id'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name', 'phone', 'department']

    def __str__(self):
        return self.id


"""



class Club(models.Model): 
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20)
    intro = models.TextField()

    def __str__(self):
        return self.name


class Recruit(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="recruits")
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    total_step = models.IntegerField()

    def __str__(self):
        return self.title
    


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager_accounts")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="managers")
    super = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + self.club.name


class Apply(models.Model):
    applier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applies")
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name="appliers")
    content = models.TextField()
    submit_at = models.DateTimeField(auto_now=True)
    temp_save = models.BooleanField(default=False)
    curr_step = models.IntegerField(default=1)


class Comment(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    apply = models.ForeignKey(Apply, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)
    line_idx = models.IntegerField(default=0)


class ApplyForm(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="forms")
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class Notice(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="notices")
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    uploaded = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    view_range = models.IntegerField(default=0)


class TimeTable(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name="time_cells")
    date_time = models.DateTimeField(unique=True)

class SelectTime(models.Model):
    apply = models.ForeignKey(Apply, on_delete=models.CASCADE, related_name="select_times")
    select_time = models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name="selected_by")
    fixed = models.BooleanField(default=False)



