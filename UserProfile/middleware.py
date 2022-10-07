import asyncio
from django.utils.decorators import sync_and_async_middleware
from .models import UserSettings
from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin


def get_settings(request):
    print('__________________________________________________')
    if request.user.is_active:
        return UserSettings.objects.get(user=request.user) 
    return None

@sync_and_async_middleware
def simple_middleware(get_response):
    # One-time configuration and initialization goes here.
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request):
            # Do something here!
            response = await get_response(request)
            #print(f'11 {response=}')
            return response

    else:
        def middleware(request):
            request.user_settings = SimpleLazyObject(lambda: get_settings(request))
            # Do something here!
            response = get_response(request)
            response.user_settings = SimpleLazyObject(lambda: get_settings(request))
            #settings = UserSettings.objects.get(user=request.user)
            #print(f'22 {response=}\t{settings}')
            #response['settings'] = settings
            return response

    return middleware


# class SimpleMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.user_settings = "123"#SimpleLazyObject(lambda: get_settings(request))# request.user.is_anonymousFalse request.user.is_anonymous
#         #if not request.user.is_anonymous:
#         #    request.user_settings = UserSettings.objects.get(user=request.user)
#         pass