from django.shortcuts import render
from .forms import ImageForm
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

@require_POST
@login_required
@csrf_exempt
def upload_image(request):
    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            return JsonResponse({'status':1})
        except Exception as e:
            print(e)
            return JsonResponse({'status':0})


@login_required
def list_image(request):
    images = Image.objects.filter(user=request.user)
    paginator = Paginator(images,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    images = current_page.object_list
    return render(request,'image/list_image.html',{"images":images,"page":current_page})

@login_required
@csrf_exempt
@require_POST
def del_image(request):
    image_id = request.POST['id']
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html',{"images":images})
