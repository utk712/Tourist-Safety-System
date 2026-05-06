from django.urls import path
from .views import sos_alert, dashboard, check_location_risk, crime_heatmap_data, crime_map, live_risk_page, sos_data,sos_map, update_location,live_tracking_page,nearest_police,get_nearest_police

urlpatterns = [
    path('sos/', sos_alert),
    path('dashboard/', dashboard),
    path('risk-check/', check_location_risk),
    path('crime-heatmap/', crime_heatmap_data),
    path('crime-map/', crime_map),
    path('live-risk/', live_risk_page),
    path('sos-data/', sos_data),
    path('sos-map/', sos_map),
    path('update-location/', update_location),
    path('live-tracking/',live_tracking_page),
    path('nearest-police/', nearest_police),
    path('nearest-police-data/',get_nearest_police)
]