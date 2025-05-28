from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Dialogue, DialoguePractice
from django.core.exceptions import PermissionDenied

class DialogueListView(ListView):
    model = Dialogue
    template_name = 'dialogues/dialogue_list.html'
    context_object_name = 'dialogues'
    paginate_by = 10

class DialogueDetailView(DetailView):
    model = Dialogue
    template_name = 'dialogues/dialogue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            practice, created = DialoguePractice.objects.get_or_create(
                user=self.request.user,
                dialogue=self.object
            )
            context['practice'] = practice
        return context

class DialogueCreateView(LoginRequiredMixin, CreateView):
    model = Dialogue
    template_name = 'dialogues/dialogue_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('dialogues:dialogue_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DialogueUpdateView(LoginRequiredMixin, UpdateView):
    model = Dialogue
    template_name = 'dialogues/dialogue_edit.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('dialogues:dialogue_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PracticeListView(LoginRequiredMixin, ListView):
    model = DialoguePractice
    template_name = 'dialogues/practice_list.html'

    def get_queryset(self):
        return DialoguePractice.objects.filter(user=self.request.user)

@login_required
def start_practice(request, pk):
    dialogue = get_object_or_404(Dialogue, pk=pk)
    # 使用update_or_create确保记录唯一性
    practice, created = DialoguePractice.objects.update_or_create(
        user=request.user,
        dialogue=dialogue,
        defaults={'practice_count': 1}
    )
    if not created:
        practice.practice_count += 1
        practice.save()
    return JsonResponse({'status': 'success'})
