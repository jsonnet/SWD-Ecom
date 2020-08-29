from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods


@require_GET
def product_list(request):
    print(request.GET.get('page', ''))
    print(request.GET.get('pagination', ''))

    # TODO use mod to calc from no of item the page and thus whats on the page


    # response = JsonResponse({'foo': 'bar'})
    return HttpResponse("what a list")


@require_http_methods(["GET", "DELETE"])
def product_details(request, product_id):
    print(product_id)
    if request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass

    return HttpResponse("More details")


@require_POST
def product_create(request):
    print(request.body)

    return HttpResponse("hey there")
