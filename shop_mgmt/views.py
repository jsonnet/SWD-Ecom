import json

from django.core import serializers
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers, patch_response_headers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from shop_mgmt.models import Partner, Product


# check Authorization: Bearer <token> with all stored in DB for each partner
def is_authenticated(request):
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
    response = HttpResponse(dtt, content_type="application/json")
    add_never_cache_headers(response)
    return response


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
        response = HttpResponse(dtt, content_type="application/json")
        add_never_cache_headers(response)
        return response

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


# curl http://localhost:8000/api/products/create -H "Authorization: Bearer abc" -H "Content-Type: application/json" -X POST --data '{"name":"test3","description":"foo", "price":"123.45", "count":"1"}'
@csrf_exempt
@require_POST
def product_create(request):
    # check if authenticated
    if not is_authenticated(request):
        return HttpResponse(status=401)

    # get bearer token
    _, token = is_authenticated(request)

    # Check for json instead of x-www-form
    if request.content_type != 'application/json':
        return HttpResponse("Please use json request", status=400)

    params = json.loads(request.body.decode('utf-8'))
    name = params.get('name')
    desc = params.get('description')
    price = params.get('price')
    sprice = params.get('special_price', '-1')
    count = params.get('count')
    image = params.get('image', '')

    # Create product
    product = Product(name=name, description=desc, price=price, special_price=sprice, count=count, image=image,
                      seller=f'p-{token}')
    try:
        product.save()
    except IntegrityError:
        return HttpResponse('Product is already present or you did something weird\n', status=409)
    except ValueError:
        return HttpResponse('Syntax error, wrong type got assigned or non at all\n', status=422)
    except:
        return HttpResponse('Syntax error when creating a product\n', status=422)

    return HttpResponse("Product created \n", status=201)
