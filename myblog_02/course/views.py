from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from .models import Course,Lesson
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm, CreateLessonForm
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.shortcuts import redirect,render
from django.views.generic.base import View,TemplateResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
# Create your views here.

class AboutView(TemplateView):
    template_name = 'course/about.html'


'''
基于类的课程列表视图
'''
class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        paginator = Paginator(courses,3)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except EmptyPage:
            current_page = paginator.page(1)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        courses = current_page.object_list

        return render(request,self.template_name,{'courses':courses,'page':current_page})


'''
Mix-in
'''
class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin,self).get_queryset()
        return qs.filter(user=self.request.user)

class UserCourseMixin(UserMixin,LoginRequiredMixin):
    model = Course
    login_url = '/account/login'

class ManageCourseListView(UserCourseMixin,ListView):
    context_object_name = 'courses'
    template_name = 'course/manage/manage_course_list.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        page = request.GET.get('page')
        courses = Course.objects.filter(user=user)
        paginator = Paginator(courses,3)
        try:
            current_page = paginator.page(page)
        except EmptyPage:
            current_page = paginator.page(1)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        courses = current_page.object_list
        return render(request,self.template_name,{"courses":courses,"page":current_page})

class CreateCourseView(UserCourseMixin,CreateView):
    fields = ['title','overview']
    template_name = 'course/manage/create_course.html'
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            try:
                new_course = form.save(commit=False)
                new_course.user = request.user
                new_course.save()
                return HttpResponse("1")
            except:
                return HttpResponse("0")
        return render(request,self.template_name,{'form':form})

class UpdateCourseView(UserCourseMixin,UpdateView):
    fields = ['title','overview']
    template_name = 'course/manage/update_course.html'
    success_url = reverse_lazy("course:manage_course")

class CreateLessonView(LoginRequiredMixin,View):
    model = Lesson
    login_url = '/account/login/'

    def get(self,request,*arg,**kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request,'course/manage/create_lesson.html',{'form':form})

    def post(self,request,*arg,**kwargs):
        form = CreateLessonForm(self.request.user,request.POST,request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")

class LessonListView(UserMixin,ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'course/manage/lesson_list.html'

    def get(self, request, *args, **kwargs):
        course_id = request.GET.get('id')
        course = Course.objects.get(id=course_id)
        lessons = Lesson.objects.filter(course = course)
        return render(request,self.template_name,{'lessons':lessons,'course':course})

class DetailLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = "/account/login/"
    template_name = 'course/manage/detail_lesson.html'
    def get(self,request,lesson_id):
        lesson = get_object_or_404(Lesson,id=lesson_id)
        return self.render_to_response({"lesson":lesson})

class StudentListLessonView(LessonListView):
    template_name = 'course/slist_lesson.html'
    def post(self,request,*args,**kwargs):

        try:
            course = Course.objects.get(id=request.POST['course_id'])
            print(course)
            course.student.add(self.request.user)
            return HttpResponse("ok")
        except:
            return HttpResponse("sorry")

class StudentDetailLessonView(DetailLessonView):
    template_name = 'course/student_lesson.html'

@login_required
@require_POST
def delete_course(request):
    if request.method == "POST":
        course_id = request.POST['id']
        course = Course.objects.get(id=course_id)
        course.delete()
        return HttpResponse("1")


'''
基于函数的课程列表视图
'''
# def course_list(request):
#     courses = Course.objects.all()
#     paginator = Paginator(courses,3)
#     page = request.GET.get('page')
#     try:
#         current_page = paginator.page(page)
#     except PageNotAnInteger:
#         current_page = paginator.page(1)
#     except EmptyPage:
#         current_page = paginator.page(1)
#
#     courses = current_page.object_list
#     return render(request,'course/course_list.html',{"courses":courses,"page":current_page})