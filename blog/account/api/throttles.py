import time

from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle


# class RegisterThrottle(SimpleRateThrottle):
#     scope = "registerThrottle"
#
#     def get_cache_key(self, request, view):
#         if request.user.is_authenticated or request.method == "GET":
#             return None
#
#         return self.cache_format % {
#             'scope': self.scope,
#             'ident': self.get_ident(request)
#         }

class RegisterThrottle(AnonRateThrottle):
    scope = "anonThrottle"

# class RegisterThrottle(SimpleRateThrottle):
#     scope = "customThrottle"
#
#     def __init__(self):
#         super().__init__()
#         self.throttle_duration = 30  # 30 saniye
#
#     def get_cache_key(self, request, view):
#         if request.user.is_authenticated or request.method == "GET":
#             return None
#
#         return self.cache_format % {
#             'scope': self.scope,
#             'ident': self.get_ident(request)
#         }
#
#     def parse_rate(self, rate):
#         """
#         Given the request rate string, return a two tuple of:
#         <allowed number of requests>, <period of time in seconds>
#         """
#         if rate is None:
#             return (None, None)
#         num, period = rate.split('/')
#         num_requests = int(num)
#         duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
#         return (num_requests, 30)

