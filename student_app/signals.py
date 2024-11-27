from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Person, Profile, Course, Enrollment, Review, Student, Instructor
from django.core.mail import send_mail


@receiver(post_save, sender=Person)
def create_profile(sender, instance, created, **kwargs):
   if created:
       Profile.objects.create(person=instance)


@receiver(post_save, sender=Person)
def save_profile(sender, instance, **kwargs):
   instance.profile.save()


@receiver(post_delete, sender=Person)
def delete_related_records(sender, instance, **kwargs):
   if hasattr(instance, 'instructor'):
       instance.instructor.delete()
   if hasattr(instance, 'student'):
       instance.student.delete()
   if hasattr(instance, 'profile'):
       instance.profile.delete()


@receiver(post_save, sender=Course)
def course_post_save(sender, instance, created, **kwargs):
   if created:
       # Notify students about the new course
       students = Student.objects.all()
       for student in students:
           send_mail(
               'New Course Available',
               f'A new course named {instance.name} is now available.',
               'from@example.com',
               [student.person.email],
               fail_silently=False,
           )


@receiver(post_delete, sender=Course)
def course_post_delete(sender, instance, **kwargs):
   # Notify students about the course deletion
   students = Student.objects.all()
   for student in students:
       send_mail(
           'Course Deleted',
           f'The course named {instance.name} has been deleted.',
           'from@example.com',
           [student.person.email],
           fail_silently=False,
       )


# Signal to handle updates on Enrollment model
@receiver(pre_save, sender=Enrollment)
def enrollment_pre_save(sender, instance, **kwargs):
   # Ensure a student cannot enroll in the same course twice
   if instance.pk is None:
       if Enrollment.objects.filter(student=instance.student, course=instance.course).exists():
           raise ValueError('Student is already enrolled in this course.')


@receiver(post_save, sender=Enrollment)
def enrollment_post_save(sender, instance, created, **kwargs):
   if created:
       # Notify student about the new enrollment
       send_mail(
           'Enrollment Confirmed',
           f'You have been enrolled in the course: {instance.course.name}.',
           'from@example.com',
           [instance.student.person.email],
           fail_silently=False,
       )


@receiver(post_delete, sender=Enrollment)
def enrollment_post_delete(sender, instance, **kwargs):
   # Notify student about the enrollment cancellation
   send_mail(
       'Enrollment Cancelled',
       f'Your enrollment in the course: {instance.course.name} has been cancelled.',
       'from@example.com',
       [instance.student.person.email],
       fail_silently=False,
   )


# Signal to handle updates on Review model
@receiver(pre_save, sender=Review)
def review_pre_save(sender, instance, **kwargs):
   # Ensure the student is enrolled in the course before they can leave a review
   if not Enrollment.objects.filter(student=instance.student, course=instance.course).exists():
       raise ValueError('Student must be enrolled in the course to leave a review.')


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
   if created:
       # Notify instructor about the new review
       send_mail(
           'New Review Received',
           f'You have received a new review for the course: {instance.course.name}.',
           'from@example.com',
           [instance.course.instructor.person.email],
           fail_silently=False,
       )


@receiver(post_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
   # Notify instructor about the review deletion
   send_mail(
       'Review Deleted',
       f'A review for the course: {instance.course.name} has been deleted.',
       'from@example.com',
       [instance.course.instructor.person.email],
       fail_silently=False,
   )



