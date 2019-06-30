from django.shortcuts import render

from .models import Station, Route


def get_route(request):
    template = 'stations.html'
    routes = Route.objects.all()
    context = {'routes': routes}
    return render(request, template, context)
    

def view_route(request):
    template = 'stations.html'
    stations = []
    centr = {}
    latitude = []
    longitude = []
    route = request.GET.get('route')
    if route:
        st_qset = Station.objects.prefetch_related('routes').filter(routes__name=route)
        for st in st_qset:
            routes = ', '.join(r.name for r in st.routes.all())
            latitude.append(float(st.latitude))
            longitude.append(float(st.longitude))
            stations.append({'name': st.name, 'latitude': st.latitude, 'longitude': st.longitude, 'route_numbers': routes})
        centr['x'] = round((sum(latitude) / len(latitude)), 8)
        centr['y'] = round((sum(longitude) / len(longitude)), 8)
    context = {'stations': stations, 'center': centr}
    print(context)
    return render(request, template, context)
