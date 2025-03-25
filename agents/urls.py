from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),

    # path('dashboard/houses', views.houses, name='houses'),
    # path('house/create/', views.house_create, name='house_create'),
    # path('house/update/<int:pk>/', views.house_update, name='house_update'),
    # path('house/delete/<int:pk>/', views.house_delete, name='house_delete'),
    # path('profile', views.profile_page, name='profile'),
    
    path('dashboard/profile', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('dashboard/house/create/',views.agent_house_create, name='house-create'),
    path('house/<uuid:pk>/', views.agent_house_detail, name='house-detail'),
    path('house/<uuid:pk>//edit/', views.agent_house_update, name='house-update'),
    path('dashboard/house-list', views.house_list, name='house-list'),

    path('dashboard/land/create/',views.agent_land_create, name='land-create'),
    path('agents/land/<uuid:pk>/', views.agent_land_detail, name='land-detail'),

   path('agents/land/<uuid:pk>/edit/', views.agent_land_update, name='land-update'),

    path('dashboard/land-list', views.land_list, name='land-list'),

    path('dashboard/com/create/',views.agent_com_create, name='com-create'),
    path('agents/com/<uuid:pk>/', views.agent_com_detail, name='com-detail'),
    path('agents/com/<uuid:pk>/edit/', views.agent_com_update, name='com-update'),

    path('dashboard/com-list', views.com_list, name='com-list'),

    path('dashboard/off/create/',views.agent_offplan_create, name='off-create'),
    path('off/<uuid:pk>//', views.agent_off_detail, name='off-detail'),
    path('off/<uuid:pk>//edit/', views.agent_off_update, name='off-update'),
    path('dashboard/off-list', views.off_list, name='off-list'),
    path('check-pin-code-messages/', views.check_pin_code_messages, name='check_pin_code_messages'),
    # path('remove-message/', views.remove_message, name='remove_message'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
]

