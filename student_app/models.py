from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Min, Max, Sum, F, Q, Value, Case, When
from django.db.models.functions import Concat


class PersonManager(BaseUserManager):
   def create_user(self, email, first_name, last_name, phone_number, address, password=None):
       if not email:
           raise ValueError('Users must have an email address')
       user = self.model(
           email=self.normalize_email(email),
           first_name=first_name,
           last_name=last_name,
           phone_number=phone_number,
           address=address,
       )
       user.set_password(password)
       user.full_clean()
       user.save(using=self._db)
       return user


   def create_superuser(self, email, first_name, last_name, phone_number, address, password=None):
       user = self.create_user(
           email,
           password=password,
           first_name=first_name,
           last_name=last_name,
           phone_number=phone_number,
           address=address,
       )
       user.is_admin = True
       user.full_clean()
       user.save(using=self._db)
       return user


class Person(AbstractBaseUser):
   email = models.EmailField(unique=True)
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   phone_number = models.CharField(max_length=15)
   address = models.CharField(max_length=255)
   is_active = models.BooleanField(default=True)
   is_admin = models.BooleanField(default=False)


   objects = PersonManager()


   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'address']


   def __str__(self):
       return self.email


class Profile(models.Model):
   person = models.OneToOneField(Person, on_delete=models.CASCADE)
   bio = models.TextField(blank=True)


   def __str__(self):
       return f"{self.person.email}'s Profile"


class Instructor(models.Model):
   person = models.OneToOneField(Person, on_delete=models.CASCADE)
   bio = models.TextField()
   salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])


   def __str__(self):
       return f"Instructor: {self.person.email}"


   @property
   def number_of_courses(self):
       return self.courses.count()


   def get_top_rated_course(self):
       return self.courses.annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating').first()


   def get_high_salary_instructors_above(self, base_salary):
        return Instructor.objects.filter(salary__gte=base_salary * 1.2)



class Course(models.Model):
   name = models.CharField(max_length=255)
   description = models.TextField()
   instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')


   def __str__(self):
       return self.name


   @property
   def number_of_students(self):
       return self.students.count()


   def get_average_rating(self):
       return self.reviews.aggregate(Avg('rating'))['rating__avg']


   def get_students_values(self):
       return self.students.values('person__first_name', 'person__last_name', 'studentcourse__marks')


   def get_high_achievers(self):
       return self.students.filter(studentcourse__marks__gte=85)


   def get_high_enrollment_courses(self):
       return Course.objects.annotate(
           num_enrollments=Count('enrollments')
       ).filter(
           Q(num_enrollments__gte=50)
       ).order_by('-num_enrollments')


   def get_concatenated_names(self):
       return self.students.annotate(
           full_name=Concat(F('person__first_name'), Value(' '), F('person__last_name'))
       ).values('full_name')


class Student(models.Model):
   person = models.OneToOneField(Person, on_delete=models.CASCADE)
   registration_number = models.CharField(max_length=30)
   courses = models.ManyToManyField(Course, through='StudentCourse', related_name='students')


   def __str__(self):
       return f"Student: {self.person.email}"


   @property
   def number_of_courses(self):
       return self.courses.count()


   def get_courses_marks(self):
       return self.studentcourse_set.values('course__name', 'marks')


   def get_marks_above_90(self):
       return self.studentcourse_set.filter(marks__gt=90).values('course__name', 'marks')


   def get_recent_courses(self):
       return self.courses.filter(studentcourse__date_enrolled__gte=F('studentcourse__date_enrolled') - timedelta(days=30))


class StudentCourse(models.Model):
   student = models.ForeignKey(Student, on_delete=models.CASCADE)
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
   date_enrolled = models.DateField(auto_now_add=True)


   class Meta:
       unique_together = ('student', 'course')


class Enrollment(models.Model):
   student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   enrollment_date = models.DateField(auto_now_add=True)


   class Meta:
       unique_together = ('student', 'course')


class Module(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
   name = models.CharField(max_length=100)
   description = models.TextField()


   def __str__(self):
       return self.name


class Review(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
   student = models.ForeignKey(Student, on_delete=models.CASCADE)
   rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
   comment = models.TextField()


   def __str__(self):
       return f"Review by {self.student.person.email} for {self.course.name}"


   class Meta:
       constraints = [
           models.UniqueConstraint(
               fields=['course', 'student'],
               name='unique_review'
           ),
           models.CheckConstraint(
               check=Q(rating__gte=1) & Q(rating__lte=5),
               name='rating_range_check'
           )
       ]



