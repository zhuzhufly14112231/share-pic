import redis
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from images.forms import ImageCreateForm
from images.models import Image
from action.utils import create_action
from django.conf import settings
# Create your views here.

r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

@login_required
def image_create(request):
    if request.method == 'POST':
        # 表单被提交
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            # 表单验证通过
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # 把当前用户附加到数据对象上
            new_item.user = request.user
            new_item.save()
            # 行为流  添加图片动作
            create_action(request.user,'添加了图片',new_item)
            messages.success(request, '图片添加成功')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    return render(request, 'images/create.html', {'section': 'images', 'form': form})


def images_detail(request, id, slug):
    """
    :url : /images/detail/
    :param request:
    :param id: 图片的id
    :param slug: 使用该图片的字段
    :return: ("image":object, "section":string)
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    # 浏览数 + 1
    # incr 将键对应的值加1
    # 如果键不存在,那么自动创建key(初始值为0),然后将值加1
    # redis数据库的key常用冒号(:)分割字符串,这样的key名容易阅读,便于对应的具体对象和查找
    total_views = r.incr('image:{}:views'.format(image.id))
    # 在有序集合image_ranking里,把image的分数加1
    r.zincrby('image_ranking',1,image.id)
    return render(request, 'images/detail.html', {'image': image, 'section': 'images','total_views':total_views})


@login_required
@require_POST
def image_like(request):
    """
    :param request:
    :return:
    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # 多对多字段的管理
            # 使用add和remove方法用来添加和删除多对多关系
            # add方法即使传入已经存在的数据对象也不会重复建立关系
            # remove方法即使传入不存在的数据对象,也不会报错
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user,'喜欢了图片',image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})



@login_required
def image_list(request):
    images = Image.objects.all()
    return render(request,'images/image_list.html',{'images': images, 'section': 'images'})


@login_required
def image_ranking(request):
    # 获得排名前10为的图片id列表
    image_rank = r.zrange('image_ranking',0,-1,desc=True)[:10]
    # 获取排名最高的图片 然后排序
    most_viewd = Image.objects.filter(id__in=image_rank)
    return render(request,'images/ranking.html',{'section':'images','most_viewd':most_viewd})


