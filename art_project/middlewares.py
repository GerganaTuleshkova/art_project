import logging

from art_project.art_portal_app.views import internal_error_view


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code >= 500:

            logging.critical('Critical: On.Art error')
            logging.error('Error: On.Art error')
            logging.warning('Warning: On.Art error')
            logging.info('Info: On.Art error')
            logging.debug('Debug: On.Art error')
            return internal_error_view(request)

        return response
    return middleware
