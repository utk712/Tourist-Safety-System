from django.urls import path
from .views import (
    sos_alert,
    dashboard,
    check_location_risk,
    crime_heatmap_data,
    crime_map,
    live_risk_page,
    sos_data,
    sos_map,
    update_location,
    live_tracking_page,
    nearest_police,
    get_nearest_police,
    ai_chat_assistant,
    search_location_api,
    tourist_spots,
    tourist_spot_detail
)

urlpatterns = [
    path('sos/', sos_alert, name='sos_alert'),
    path('dashboard/', dashboard, name='dashboard'),
    path('risk-check/', check_location_risk, name='check_location_risk'),
    path('crime-heatmap/', crime_heatmap_data, name='crime_heatmap_data'),
    path('crime-map/', crime_map, name='crime_map'),
    path('live-risk/', live_risk_page, name='live_risk_page'),
    path('sos-data/', sos_data, name='sos_data'),
    path('sos-map/', sos_map, name='sos_map'),
    path('update-location/', update_location, name='update_location'),
    path('live-tracking/', live_tracking_page, name='live_tracking_page'),
    path('nearest-police/', nearest_police, name='nearest_police'),
    path('nearest-police-data/', get_nearest_police, name='get_nearest_police'),
    path('search-location/', search_location_api, name='search_location_api'),
    path('ai-chat/', ai_chat_assistant, name='ai_chat'),
    path('tourist-spots/', tourist_spots, name='tourist_spots'),
    path('tourist-spot/<str:spot_id>/', tourist_spot_detail, name='tourist_spot_detail'),
]