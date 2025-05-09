# # myproject/middleware.py
# from django.contrib.auth import logout
# from django.urls import reverse

# class LogoutEveryPageMiddleware:
#     """
#     Logs out any authenticated user after each response,
#     except for login/logout endpoints.
#     """
#     EXEMPT_URLS = {
#         reverse('login'),
#         reverse('logout'),
#         reverse('admin:login'),
#     }

#     #This runs at the time of when server starts
#     def __init__(self, get_response):
#         self.get_response = get_response

#     #This function is called eveyrtime when a request is made
#     #It is used to process the request before it reaches the view
#     def __call__(self, request):
#         response = self.get_response(request)

#         # If the user was authenticated and they did NOT just visit an exempt URL...
#         if request.user.is_authenticated and request.path not in self.EXEMPT_URLS:
#             logout(request)

#         return response
