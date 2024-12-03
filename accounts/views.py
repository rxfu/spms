from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView
from unfold.views import UnfoldModelAdminViewMixin

from accounts.forms import RegisterForm, UserAuthenticationForm
from accounts.models import Profile
from spms import settings


# Create your views here.

class RegisterView(UnfoldModelAdminViewMixin, SuccessMessageMixin, CreateView):
    title = '注册'
    permission_required = ()
    template_name = "admin/register.html"
    form_class = RegisterForm
    success_url = "/"
    success_message = "用户注册成功！"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_staff = True
        self.object.is_active = True
        self.object.save()

        group = Group.objects.get(id=settings.G_APPLICANT)
        self.object.groups.add(group)

        return super().form_valid(form)


class UserLoginView(UnfoldModelAdminViewMixin, LoginView):
    title = '登录'
    permission_required = ()
    template_name = "admin/login.html"
    form_class = UserAuthenticationForm

    def get_success_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(id=settings.G_APPLICANT).exists():
                if hasattr(self.request.user, 'profile'):
                    return reverse_lazy('admin:project_list')
                    # return reverse_lazy("admin:accounts_profile_change",
                    #                     kwargs={"object_id": Profile.objects.get(user=self.request.user).id})
                else:
                    return reverse_lazy('admin:accounts_profile_add')
            elif self.request.user.groups.filter(id=settings.G_COLLEGE).exists():
                return reverse_lazy("admin:projects_information_changelist")
            elif self.request.user.groups.filter(id=settings.G_PANELIST).exists():
                return reverse_lazy("admin:reviews_review_changelist")

        return super().get_success_url()


class ProfileRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                if hasattr(self.request.user, 'profile'):
                    redirect = reverse_lazy("admin:accounts_profile_change",
                                            kwargs={"object_id": Profile.objects.get(user=self.request.user).id})
                else:
                    redirect = reverse_lazy('admin:accounts_profile_add')
            else:
                redirect = reverse_lazy('admin:accounts_profile_changelist')

            return redirect
