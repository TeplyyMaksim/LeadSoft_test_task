from pyramid.view import (
    view_config,
    view_defaults,
)
from .parse_all_stuff import main_function

@view_defaults(renderer='home.jinja2')
class HomeView:
    def __init__(self, request):
        self.request = request
    
    @view_config(route_name='home')
    def home(self):
        return {'name': 'Input price range'}
    

@view_defaults(renderer='results.jinja2')
class ResultView:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='results')
    def results(self):
        pricefrom = self.request.params.get('pricefrom', 0)
        priceto = self.request.params.get('priceto', '')
        if pricefrom == '':
            pricefrom = 0
            
        # validation
        if (priceto == ''):
            parsed_information = main_function(pricefrom)
        else:
            parsed_information = main_function(pricefrom, priceto)
            
        counter = len(parsed_information)
        
        # output data
        return {
            'pricefrom': pricefrom,
            'priceto': priceto,
            'counter': counter,
            'data': parsed_information,
        }


#   GET view example
#def plain(self):
#    name = self.request.params.get('name', 'No Name Provided')
#    
#    body = 'URL %s with name: %s' % (self.request.url, name)    # The strangest content filling ever
#    return Response(
#        content_type='text/plain',
#        body=body,
#    )

#   Function based view example
# First view on http://localhost:6543/ in Function based view
# @view_config(route_name='home', renderer='home.pt')
# def home(request):
#     return {'name': 'Home View'}