from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Course, Category
from .forms import CourseForm
from django.http import JsonResponse

def api_courses(request):
    course = Course.objects.all().order_by('-year', 'title')
    data = [
        {
            'id': c.pk,
            'title': c.title,
            'instructor': c.instructor,
            'year': c.year,
            'category': c.category.name,
        }
        for c in course
    ]
    return JsonResponse(data, safe=False)
    
def api_course_detail(request, pk):
    course=get_object_or_404(Course, pk=pk)
    data={
            'id': course.pk,
            'title': course.title,
            'instructor': course.instructor,
            'year': course.year,
            'category': course.category.name,
         }
    return JsonResponse(data)
    
def course_list(request):
    courses = Course.objects.all().order_by('-year', 'title')
    categories = Category.objects.all().order_by('name')

    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)

    query = request.GET.get('q', '')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(instructor__icontains=query)
        )

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})
    
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    courses_in_category = Course.objects.filter(category=category)
    
    return render(request, 'courses/course_category.html', {
        'category': category,
        'courses': courses_in_category
    })


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Add'})
    
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Edit'})
    
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})
            
