"""
Enrollments Service
"""


from common.djangoapps.student.models import CourseEnrollment


class EnrollmentsService(object):
    """
    Enrollments service

    Provides functions related to course enrollments
    """

    # def get_active_enrollments_by_course(self, course_id):
    #     """
    #     Returns a list of active enrollments for a course
    #     """
    #     return list(CourseEnrollment.objects.filter(course_id=course_id, is_active=True))

    def get_active_enrollments_by_course(self, course_id):
        """
        Returns a list of active enrollments for a course
        """
        return CourseEnrollment.objects.filter(course_id=course_id, is_active=True)


    def get_active_enrollments_by_course_users_can_take_proctored_exams(self, course_id):
        import pudb; pu.db
        from django.db.models import Q
        from common.djangoapps.course_modes.models import CourseMode
        from django.conf import settings
        from xmodule.modulestore.django import modulestore
        from opaque_keys.edx.keys import CourseKey
        from operator import _or

        course_id = CourseKey.from_string(course_id)
        course_module = modulestore().get_course(course_id)
        if not course_module or not course_module.enable_proctored_exams:
            return None

        enrollments = CourseEnrollment.objects.filter(course_id=course_id, is_active=True)

        # Only allow paid modes
        appropriate_modes = [
            CourseMode.VERIFIED,
            CourseMode.MASTERS,
            CourseMode.PROFESSIONAL,
            CourseMode.EXECUTIVE_EDUCATION,
        ]
        
        # If the proctoring provider allows learners in honor mode to take exams, include it
        if settings.PROCTORING_BACKENDS.get(course_module.proctoring_provider, {}).get('allow_honor_mode'):
            appropriate_modes.append(CourseMode.HONOR)

        q_objects_modes = reduce(_or, [Q(mode=mode) for mode in appropriate_modes])


  




        # q_objects_modes = [
        #     Q(mode__slug=mode) for mode in appropriate_modes
        # ]
        # q_objects_modes = Q(mode=CourseMode.VERIFIED) | Q(mode=CourseMode.MASTERS) | Q(mode=CourseMode.PROFESSIONAL) | Q(mode=CourseMode.EXECUTIVE_EDUCATION)

        enrollments = enrollments.filter(q_objects_modes)
        enrollments = enrollments.select_related('user')
        return enrollments
