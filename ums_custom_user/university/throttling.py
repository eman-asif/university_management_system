from rest_framework.throttling import UserRateThrottle

class StudentThrottle(UserRateThrottle):
    scope = 'student'

class FacultyThrottle(UserRateThrottle):
    scope = 'faculty'

class AdminThrottle(UserRateThrottle):
    scope = 'admin'
