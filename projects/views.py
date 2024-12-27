from django.urls import reverse_lazy
from django.views.generic import RedirectView
from wkhtmltopdf.views import PDFTemplateView

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


class ApplicationGenerateView(PDFTemplateView):
    filename = 'application.pdf'
    template_name = 'admin/projects/information/pdf.html'
    cmd_options = {
        'enable-local-file-access': True,
    }

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['project'] = Information.objects.get(pk=pk)
        context['setting'] = Setting.objects.get(is_opened=True, phase_id=1)

        return context
