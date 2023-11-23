from django.shortcuts import render

def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    response.context = {'message': 'Упс, цієї сторінки не існує'}
    return response

def handler403(request, exception, template_name='403.html'):
    response = render(request, template_name)
    response.status_code = 403
    response.context = {'message': 'У вас немає доступу до цієї фунції.\nМожливо потрібно увійти до аккаунту'}
    return response