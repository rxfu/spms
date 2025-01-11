from django.urls import reverse_lazy
from django.views.generic import RedirectView, DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from unfold.views import UnfoldModelAdminViewMixin

from projects.models import Information
from settings.models import Setting
from spms import settings


# Create your views here.
class InformationRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(id=settings.G_APPLICANT).exists():
                setting = Setting.objects.get(is_opened=True)

                if Information.objects.filter(year=setting.year, applicant=self.request.user).exists():
                    project = Information.objects.get(year=setting.year, applicant=self.request.user)

                    redirect = reverse_lazy("admin:projects_information_change", kwargs={"object_id": project.id})
                else:
                    redirect = reverse_lazy('admin:projects_information_add')
            else:
                redirect = reverse_lazy('admin:projects_information_changelist')

            return redirect


class ApplicationGenerateView(WeasyTemplateResponseMixin, DetailView):
    pdf_filename = 'application.pdf'
    template_name = 'admin/projects/information/pdf.html'
    model = Information
    context_object_name = 'project'
    pdf_options = {'pdf_variant': 'pdf/ua-1'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting'] = Setting.objects.get(is_opened=True, phase_id=1)

        return context


class ApplicationPreviewView(UnfoldModelAdminViewMixin, DetailView):
    title = '预览'
    permission_required = ()
    template_name = 'admin/projects/information/preview.html'
    model = Information
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting'] = Setting.objects.get(is_opened=True, phase_id=1)

        return context
