from rest_framework import serializers
from .models import Person, Profile, Instructor, Student, Course, Module, Enrollment, Review, StudentCourse
from django.core.validators import RegexValidator


# Phone number validator
phone_regex = RegexValidator(regex=r'^\+\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class PersonSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex])
    class Meta:
       model = Person
       fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password']
       extra_kwargs = {
           'password': {'write_only': True},
       }
    def create(self, validated_data):
       person = Person(**validated_data)
       person.full_clean()  # Ensuring the data is valid before saving
       person.save()
       return person


    def update(self, instance, validated_data):
       for attr, value in validated_data.items():
           if attr == 'password':
               instance.set_password(value)
           else:
               setattr(instance, attr, value)
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()
       return instance


class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = Profile
       fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
   instructor = serializers.SlugRelatedField(slug_field='person__email', queryset=Instructor.objects.all())


   class Meta:
       model = Course
       fields = ['id', 'name', 'description', 'instructor']


   def to_representation(self, instance):
       response = super().to_representation(instance)
       response['instructor'] = {
           'id': instance.instructor.person.id,
           'email': instance.instructor.person.email,
           'first_name': instance.instructor.person.first_name,
           'last_name': instance.instructor.person.last_name
       }
       return response


class InstructorSerializer(serializers.ModelSerializer):
   person = serializers.SlugRelatedField(slug_field='email', queryset=Person.objects.all())
   courses = CourseSerializer(many=True, read_only=True)


   class Meta:
       model = Instructor
       fields = ['person', 'bio', 'salary', 'courses']


   def validate_person(self, value):
       if Instructor.objects.filter(person=value).exists() or Student.objects.filter(person=value).exists():
           raise serializers.ValidationError("This user is already associated with an Instructor or Student.")
       return value


   def to_representation(self, instance):
       response = super().to_representation(instance)
       response['person'] = PersonSerializer(instance.person).data
       return response


class StudentCourseSerializer(serializers.ModelSerializer):
   class Meta:
       model = StudentCourse
       fields = ['student', 'course', 'marks', 'date_enrolled']


class StudentSerializer(serializers.ModelSerializer):
   person = serializers.SlugRelatedField(slug_field='email', queryset=Person.objects.all())
   courses = StudentCourseSerializer(many=True, read_only=True)


   class Meta:
       model = Student
       fields = ['person', 'registration_number', 'courses']


   def validate_person(self, value):
       if Student.objects.filter(person=value).exists() or Instructor.objects.filter(person=value).exists():
           raise serializers.ValidationError("This user is already associated with an Instructor or Student.")
       return value


   def to_representation(self, instance):
       response = super().to_representation(instance)
       response['person'] = PersonSerializer(instance.person).data
       response['courses'] = StudentCourseSerializer(instance.studentcourse_set.all(), many=True).data
       return response


class EnrollmentSerializer(serializers.ModelSerializer):
   student = serializers.SlugRelatedField(slug_field='email', queryset=Person.objects.all())
   course = CourseSerializer()


   class Meta:
       model = Enrollment
       fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
   course = CourseSerializer()


   class Meta:
       model = Module
       fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
   course = CourseSerializer()
   student = StudentSerializer()


   class Meta:
       model = Review
       fields = '__all__'



