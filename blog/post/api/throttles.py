from rest_framework.throttling import UserRateThrottle


class PostListThrottle(UserRateThrottle):
    scope = "customThrottle"
