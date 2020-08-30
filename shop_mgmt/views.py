import json

from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# FIXME
#  check for proper HTTP response codes on error
#  require decorators already throw 405 on error
from shop_mgmt.models import Partner, Product


def is_authenticated(request):
    # check Authorization: Bearer <token> with all stored in DB for each partner

    # check if Authorization header is present
    if 'Authorization' not in request.headers.keys():
        return False

    # get token part from header
    bearer = request.headers['Authorization'].split(' ')[1]

    # find a corresponding partner object
    try:
        Partner.objects.get(token=bearer)
    except Partner.DoesNotExist:
        return False
    else:
        return True, bearer


@require_GET
def product_list(request):
    # check if authenticated
    if not is_authenticated(request):
        return HttpResponse(status=401)

    # get bearer token
    _, token = is_authenticated(request)

    # get GET params (default 0 for int() )
    page = int(request.GET.get('page', '0'))
    paginator = int(request.GET.get('paginator', '0'))

    # get all products from shop and requesting partner
    dt = Product.objects.filter(Q(seller=0) | Q(seller=f'p-{token}'))

    # if we have a paginator set limit/offset the result
    if paginator:
        dt = dt[(page - 1) * paginator: page * paginator]

    # serialize to json and nice indent
    dtt = serializers.serialize("json", dt, indent=2)

    # Dont want to use JsonResponse
    return HttpResponse(dtt, content_type="application/json")


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def product_details(request, product_id):
    # check if authenticated
    if not is_authenticated(request):
        return HttpResponse(status=401)

    # get bearer token
    _, token = is_authenticated(request)

    if request.method == 'GET':
        # get all products from shop and requesting partner
        dt = Product.objects.filter(Q(seller=0) | Q(seller=f'p-{token}'))

        # add filter for product id
        dt = dt.filter(slug=product_id)

        # serialize to json and nice indent
        dtt = serializers.serialize("json", dt, indent=2)

        # Dont want to use JsonResponse
        return HttpResponse(dtt, content_type="application/json")

    elif request.method == 'DELETE':
        # get all products from requesting partner
        dt = Product.objects.filter(seller=f'p-{token}')

        # add filter for product id and delete object
        count, _ = dt.filter(slug=product_id).delete()

        # check if an object was actually deleted else return error
        if count == 0:
            return HttpResponse(f"No object found for {product_id}\n", status=404)

        return HttpResponse(f"Object {product_id} gone forever\n", status=200)

    return HttpResponse(status=404)


# TODO check if everything here is correct
@csrf_exempt
@require_POST
def product_create(request):
    # check if authenticated
    if not is_authenticated(request):
        return HttpResponse(status=401)

    # get bearer token
    _, token = is_authenticated(request)

    print(request.POST)

    name = request.POST.get('name')
    desc = request.POST.get('description')
    price = request.POST.get('price')
    sprice = request.POST.get('special_price', '-1')
    count = request.POST.get('count')
    image = request.POST.get('image', '')

    product = Product(name=name, description=desc, price=price, special_price=sprice, count=count, image=image,
                      seller=f'p-{token}')
    try:
        product.save()
    except:
        return HttpResponse('Syntax error when creating a product \n', status=422)

    # TODO name, description, price, special_price (?), count, image, seller (? - or from access token?)
    #  takes these from the request#body and create a new object in DB (just like with users)
    #  is only used by partners so seller always p-<id> s.t. we could use the token to identify
    #  on semantic error 422 or 400
    # curl http://localhost:8000/api/products/create -H "Authorization: Bearer abc" -H "Content-Type: application/x-www-form-urlencoded" -X POST --data 'name=test&desc=more'

    return HttpResponse("Product created \n", status=201)
