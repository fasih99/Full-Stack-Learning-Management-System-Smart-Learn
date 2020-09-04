from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.students.filter(id=request.user.id).exists()

# We subclass the BasePermission class and override the
# has_object_permission(). We check that the user
# performing the request is present in the students
# relationship of the Course
# object. We are going to use the IsEnrolled permission next.
