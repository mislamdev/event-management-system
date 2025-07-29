from django.urls import path
from event_app.views import organizer_dashboard, EventListView, EventDetailView, EventCreateView, EventUpdateView, \
    EventDeleteView, ParticipantListView, ParticipantDetailView, ParticipantCreateView, ParticipantUpdateView, \
    ParticipantDeleteView, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView

urlpatterns = [
    # Dashboard
    path('', organizer_dashboard, name='organizer-dashboard'),

    # Event URLs
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/add/', EventCreateView.as_view(), name='event-add'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    # Participant URLs
    path('participants/', ParticipantListView.as_view(), name='participant-list'),
    path('participants/<int:pk>/', ParticipantDetailView.as_view(), name='participant-detail'),
    path('participants/add/', ParticipantCreateView.as_view(), name='participant-add'),
    path('participants/<int:pk>/edit/', ParticipantUpdateView.as_view(), name='participant-edit'),
    path('participants/<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant-delete'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]
