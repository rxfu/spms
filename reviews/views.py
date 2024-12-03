from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin

from projects.models import Information
from reviews.models import Review
from spms import settings


# Create your views here.
class ReviewProjectView(UnfoldModelAdminViewMixin, SuccessMessageMixin, TemplateView):
    title = '评审'
    permission_required = ()
    template_name = 'admin/reviews/review/change_form.html'
    success_url = "/"
    success_message = "用户注册成功！"


class ReviewRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(id=settings.G_PANELIST).exists():
                project = Information.objects.get(id=kwargs['project_id'])

                if Review.objects.filter(year='2024', project=project, panelist=self.request.user).exists():
                    review = Review.objects.get(year='2024', project=project, panelist=self.request.user)

                    redirect = reverse_lazy("admin:reviews_review_change", kwargs={"object_id": review.id})
                else:
                    redirect = reverse_lazy('admin:reviews_review_add') + '?project_id=' + str(kwargs['project_id'])
            else:
                redirect = reverse_lazy('admin:reviews_review_changelist')

            return redirect
