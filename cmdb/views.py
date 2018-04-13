from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
# Create your views here.
from cmdb import models
from django.template import Context
from cmdb.models import gallery
from cmdb.models import artist
from cmdb.models import image
from cmdb.models import detail
from unit.indexing import *


invertedindex = read_index('unit/index.txt')


@csrf_exempt
def webSearch(request):
    search = request.POST['search']
    result = {}
    result['out'] = output(search, invertedindex)
    return render(request, "webSearch.html", result)

@csrf_exempt
def home(request):
    return render(request, "home.html")


def index(request):
    gall = gallery.objects.all()
    result = {}
    result['info'] = gall
    result['nu'] = '123'
    return render(request, "index.html", result)


def galleries(request):
    gall = gallery.objects.all()
    result = {}
    result['info'] = gall
    return render(request, "gallery.html", result)


@csrf_exempt
def images(request):
    id = request.GET['id']
    ima = image.objects.filter(gallery_id=id)
    gal = gallery.objects.get(gallery_id=id)
    result = {}
    result['gid'] = id
    result['ginfo'] = gal
    if ima.count() == 0:
        result['info'] = 0
    else:
        result['info'] = ima
    return render(request, "image.html", result)


def artists(request):
    id = request.GET['id']
    art = artist.objects.get(artist_id=id)
    result = {}
    result['art'] = art
    iid = request.GET['iid']
    result['iid'] = iid
    return render(request, "artist.html", result)


def newimage(request):
    id=request.GET['id']
    result = {}
    result['gid'] = id
    art = artist.objects.all()
    result['art'] = art
    return render(request, "newimage.html", result)


def newartist(request):
    return render(request, "newartist.html")


def newgallery(request):
    return render(request, "newgallery.html")


def details(request):
    image_id = request.GET['image_id']
    det = detail.objects.get(image_id=image_id)
    ima = image.objects.get(image_id=image_id)
    art = artist.objects.filter(artist_id=ima.artist_id)
    result = {}
    result['infod'] = det
    result['infoi'] = ima
    result['len'] = len(art)
    if len(art) == 0:
        result['art'] = 0
    else:
        result['art'] = art[0]
    return render(request, "detail.html", result)


@csrf_exempt
def insert(request):
    kind = request.GET['kind']
    if kind == '1':
        gallery_name = request.POST['gallery_name']
        gallery_description = request.POST['gallery_description']
        result = {}
        result['kind'] = 1
        if gallery_name == '':
            result['info'] = 0
            return render(request, "insert.html", result)
        if gallery_description == '':
            description = 'none'
        if len(gallery_name) > 45 or len(gallery_description) > 2000:
            result['info'] = 0
        else:
            gallery.objects.create(name=gallery_name, description=gallery_description)
            result['info'] = 1
        return render(request, "insert.html", result)
    elif kind == '2':
        gid = request.GET['gid']
        title = request.POST['title']
        link = request.POST['link']
        artist_id = request.POST['artist_id']
        year = request.POST['year']
        type = request.POST['type']
        width = request.POST['width']
        height = request.POST['height']
        location = request.POST['location']
        description = request.POST['description']
        result = {}
        result['info'] = 1
        result['kind'] = 2
        result['gid'] = gid
        if title == '':
            title = 'unknown'
        else:
            if len(title) > 45:
                result['info'] = 0
        if location == '':
            location = 'unknown'
        if description == '':
            description = 'none'
        if height == '':
            height = None
        if width == '':
            width = None
        if year == '':
            year = None
        if type == '':
            type = 'unknown'
        if link == '':
            result['info'] = 0
            return render(request, "insert.html", result)
        else:
            if len(link) > 200:
                result['info'] = 0
                return render(request, "insert.html", result)
        if artist_id == '-1':
            image.objects.create(title=title, link=link, artist_id=None, gallery_id=gid)
        else:
            image.objects.create(title=title, link=link, artist_id=artist_id, gallery_id=gid)
        ima = image.objects.filter(title=title, link=link)
        detail.objects.create(image_id=ima[0].image_id, year=year, type=type, width=width, height=height, location=location, description=description)
        det = detail.objects.filter(image_id=ima[0].image_id)
        image.objects.filter(image_id=ima[0].image_id).update(detail_id=det[0].detail_id)
        return render(request, "insert.html", result)
    elif kind == '3':
        name = request.POST['name']
        birth_year = request.POST['birth_year']
        country = request.POST['country']
        description = request.POST['description']
        result = {}
        result['info'] = 1
        result['kind'] = 3
        if name == '':
            result['info'] = 0
        else:
            if len(name) > 45:
                result['info'] = 0
                return render(request, "insert.html", result)
        if birth_year == '':
            birth_year = 'unknown'
        if country == '':
            country = 'unknown'
        if description == '':
            description = 'none'
        else:
            if len(description) > 45:
                result['info'] = 0
                return render(request, "insert.html", result)
        artist.objects.create(name=name, birth_year=birth_year, country=country, description=description)
        return render(request, "insert.html", result)


@csrf_exempt
def delete(request):
    kind = request.GET['kind']
    if kind == '1':
        gallery_name_delete = request.POST['gallery_name_delete']
        state = gallery.objects.filter(name=gallery_name_delete).delete()
        result = {}
        #print(state[0])
        if state[0] == 0:
            result['info'] = 0
        else:
            result['info'] = 1
        return render(request, 'delete.html', result)
    if kind == '2':
        image_id = request.GET['image_id']
        gallery_id = request.GET['gallery_id']
        state1 = image.objects.filter(image_id=image_id).delete()
        state2 = detail.objects.filter(image_id=image_id).delete()
        result = {}
        if state1[0] == 0 or state2[0] == 0:
            result['info'] = 0
        else:
            result['info'] = 1
        result['gid'] = gallery_id
        result['iid'] = image_id
        result['kind'] = 2
        return render(request, 'delete.html', result)


@csrf_exempt
def update(request):
    kind = request.GET['kind']
    if kind == '1':
        gallery_id = request.GET['id']
        gallery_name = request.POST['gallery_name']
        gallery_description = request.POST['gallery_description']
        state = 0
        if gallery_name != '':
            gallery.objects.filter(gallery_id=gallery_id).update(name=gallery_name)
            state = 1
        if gallery_description != '':
            gallery.objects.filter(gallery_id=gallery_id).update(description=gallery_description)
            state = 1
        result = {}
        if state == 0:
            result['info'] = 0
        else:
            result['info'] = 1
        result['kind'] = 1
        result['gid'] = gallery_id
        return render(request, 'update.html', result)
    elif kind == '2':
        image_id = request.GET['iid']
        title = request.POST['title']
        link = request.POST['link']
        artist_id = request.POST['artist_id']
        year = request.POST['year']
        type = request.POST['type']
        width = request.POST['width']
        height = request.POST['height']
        location = request.POST['location']
        description = request.POST['description']
        state = 0
        if title != '':
            image.objects.filter(image_id=image_id).update(title=title)
            state = 1
        if link != '':
            image.objects.filter(image_id=image_id).update(link=link)
            state = 1
        if artist_id != '':
            if artist_id == '-1':
                image.objects.filter(image_id=image_id).update(artist_id=None)
            else:
                image.objects.filter(image_id=image_id).update(artist_id=artist_id)
            state = 1
        if year != '':
            detail.objects.filter(image_id=image_id).update(year=year)
            state = 1
        if type != '':
            detail.objects.filter(image_id=image_id).update(type=type)
            state = 1
        if width != '':
            detail.objects.filter(image_id=image_id).update(width=width)
            state = 1
        if height != '':
            detail.objects.filter(image_id=image_id).update(heigth=height)
            state = 1
        if location != '':
            detail.objects.filter(image_id=image_id).update(location=location)
            state = 1
        if description != '':
            detail.objects.filter(image_id=image_id).update(description=description)
            state = 1
        result = {}
        if state == 0:
            result['info'] = 0
        else:
            result['info'] = 1
        result['kind'] = 2
        result['iid'] =image_id
        return render(request, 'update.html', result)
    elif kind == '3':
        artist_id = request.GET['id']
        name = request.POST['name']
        birth_year = request.POST['birth_year']
        country = request.POST['country']
        description = request.POST['description']
        state = 0
        if name != '':
            artist.objects.filter(artist_id=artist_id).update(name=name)
            state = 1
        if birth_year != '':
            artist.objects.filter(artist_id=artist_id).update(birth_year=birth_year)
            state = 1
        if country != '':
            artist.objects.filter(artist_id=artist_id).update(country=country)
            state = 1
        if description != '':
            artist.objects.filter(artist_id=artist_id).update(description=description)
            state = 1
        result = {}
        if state == 0:
            result['info'] = 0
        else:
            result['info'] = 1
        result['kind'] = 3
        result['aid'] = artist_id
        return render(request, 'update.html', result)


@csrf_exempt
def Modifyimage(request):
    id = request.GET['id']
    result = {}
    result['iid'] = id
    art = artist.objects.all()
    result['art'] = art
    return render(request, 'modifyimage.html', result)


@csrf_exempt
def Modifyartist(request):
    id = request.GET['id']
    iid = request.GET['iid']
    result = {}
    result['id'] = id
    result['iid'] = iid
    return render(request, 'modifyartist.html', result)


@csrf_exempt
def Modifygallery(request):
    id = request.GET['id']
    result = {}
    result['id'] = id
    return render(request, 'modifygallery.html', result)


@csrf_exempt
def search(request):
    search = request.POST['search']
    kind = request.POST['kind']
    if search == '':
        return render(request, 'index.html')
    result = {}
    if kind == 'type':
        type = detail.objects.filter(type=search)
        result['typelen'] = len(type)
        if len(type) == 0:
            result['type'] = 0
        else:
            for i in range(0, len(type)):
                im = image.objects.get(image_id=type[i].image_id)
                result.setdefault('type', []).append(im)
    else:
        result['typelen'] = 0
    if kind == 'artist_name':
        artist_name = artist.objects.filter(name=search)
        result['artlen'] = len(artist_name)
        if len(artist_name) == 0:
            result['art'] = 0
        else:
            for i in range(0, len(artist_name)):
                im = image.objects.get(artist_id=artist_name[i].artist_id)
                result.setdefault('art', []).append(im)
    else:
        result['artlen'] = 0
    if kind == 'location':
        location = detail.objects.filter(location=search)
        result['loclen'] = len(location)
        if len(location) == 0:
            result['loc'] = 0
        else:
            for i in range(0, len(location)):
                im = image.objects.get(image_id=location[i].image_id)
                result.setdefault('loc', []).append(im)
    if kind == 'country':
         country = artist.objects.filter(country=search)
         result['coulen'] = len(country)
         if len(country) == 0:
            result['cou'] = 0
         else:
            result['cou'] = country
    if kind == 'birth_year':
         birth_year = artist.objects.filter(birth_year=search)
         result['birlen'] = len(birth_year)
         if len(birth_year) == 0:
            result['bir'] = 0
         else:
            result['bir'] = birth_year
    return render(request, 'search.html', result)
