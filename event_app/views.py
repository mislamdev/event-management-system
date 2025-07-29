from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
import datetime


class EventListView(ListView):
    model = Event
    template_name = 'event_app/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Event.objects.select_related('category').prefetch_related('participants')

        # Search by name or location [cite: 16, 17]
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(location__icontains=search_query)
            )

        # Filter by category [cite: 7]
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by date range [cite: 7]
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_app/event_detail.html'

    def get_queryset(self):
        # Prefetch participants for the detail view [cite: 6, 9]
        return super().get_queryset().prefetch_related('participants')


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_app/generic_form.html'
    success_url = reverse_lazy('event-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Event'
        return context


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_app/generic_form.html'
    success_url = reverse_lazy('event-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Event'
        return context


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_app/event_confirm_delete.html'
    success_url = reverse_lazy('event-list')


# Organizer Dashboard View
def organizer_dashboard(request):
    total_participants = Participant.objects.count()  # [cite: 12]
    total_events = Event.objects.count()  # [cite: 13]
    now = timezone.now()
    today = now.date()

    upcoming_events_count = Event.objects.filter(date__gte=today).count()  # [cite: 13]
    past_events_count = Event.objects.filter(date__lt=today).count()  # [cite: 13]

    events_today = Event.objects.filter(date=today).select_related('category')  # [cite: 14]

    # Dynamic filtering for the events list [cite: 15]
    filter_type = request.GET.get('filter', 'today')
    if filter_type == 'total':
        events_list = Event.objects.all().select_related('category')
    elif filter_type == 'upcoming':
        events_list = Event.objects.filter(date__gte=today).select_related('category')
    elif filter_type == 'past':
        events_list = Event.objects.filter(date__lt=today).select_related('category')
    else:  # Default to today's events
        events_list = events_today

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'events_today': events_today,
        'events_list': events_list,
        'filter_type': filter_type,
    }
    return render(request, 'event_app/organizer_dashboard.html', context)


# Participant Views (CRUD) [cite: 3]
class ParticipantListView(ListView):
    model = Participant
    template_name = 'event_app/participant_list.html'


class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'event_app/participant_detail.html'


class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'event_app/generic_form.html'
    success_url = reverse_lazy('participant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Participant'
        return context


class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'event_app/generic_form.html'
    success_url = reverse_lazy('participant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Participant'
        return context


class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'event_app/participant_confirm_delete.html'
    success_url = reverse_lazy('participant-list')


# Category Views (CRUD) [cite: 3]
class CategoryListView(ListView):
    model = Category
    template_name = 'event_app/category_list.html'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'event_app/category_detail.html'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'event_app/generic_form.html'
    success_url = reverse_lazy('category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Category'
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'event_app/generic_form.html'
    success_url = reverse_lazy('category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Category'
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'event_app/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
