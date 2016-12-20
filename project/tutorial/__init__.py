from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.add_route('results', '/results')
    config.add_static_view(name='static', path='tutorial:static')
    config.scan('.views')                       # Search for file .views
    return config.make_wsgi_app()