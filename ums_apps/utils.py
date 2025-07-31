from accounts.throttling import StudentThrottle, FacultyThrottle, AdminThrottle

def get_user_throttle(user):
    if user.is_authenticated:
        if user.user_type == 'student':
            return [StudentThrottle()]
        elif user.user_type == 'faculty':
            return [FacultyThrottle()]
        elif user.user_type == 'admin':
            return [AdminThrottle()]
    return []