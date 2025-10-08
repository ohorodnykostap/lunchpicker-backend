class BuildVersionMiddleware:
    '''
    Додає request.build_version (string) з заголовка X-Build-Version.
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            build_version = request.headers.get('X-Build-Version')
            if build_version and hasattr(request.user, 'employee'):
                employee = request.user.employee
                if employee.app_version != build_version:
                    employee.app_version = build_version
                    employee.save(update_fields=['app_version'])
        response = self.get_response(request)
        return response
