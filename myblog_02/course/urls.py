from django.urls import path
from django.views.generic import TemplateView
from .views import AboutView,CourseListView,ManageCourseListView,CreateCourseView,UpdateCourseView,CreateLessonView
from .views import LessonListView,DetailLessonView,StudentListLessonView,StudentDetailLessonView
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('about/',AboutView.as_view(),name='about'),
    path('course-list',CourseListView.as_view(),name="course_list"),
    path('manage-course',ManageCourseListView.as_view(),name="manage_course"),
    path('create-course',CreateCourseView.as_view(),name='create_course'),
    path('delete-course',views.delete_course,name='delete_course'),
    path('update-course/<int:pk>/',UpdateCourseView.as_view(),name='update_course'),
    path('create-lesson/',CreateLessonView.as_view(),name='create_lesson'),
    path('lesson-list/',LessonListView.as_view(),name='lesson_list'),
    path('lesson-detail/<int:lesson_id>/',DetailLessonView.as_view(),name='lesson_detail'),
    path('student-lesson-list/',StudentListLessonView.as_view(),name='student_lesson'),
    path('student-lesson-detail/<int:lesson_id>',StudentDetailLessonView.as_view(),name='student_lesson_detail')
]


'''
装饰器实现登录跳转
'''
# path('manage-course',login_required(ManageCourseListView.as_view()),name="manage_course")