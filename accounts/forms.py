from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from unfold.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminEmailInputWidget, UnfoldAdminPasswordInput, \
    UnfoldAdminSelectWidget

from accounts.models import Profile
from accounts.validators import IDValidator
from settings.models import Gender, Idtype, Education, Degree, Title, Department, Setting
from spms import settings


class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        now = datetime.now()

        if not user.is_superuser:
            if Setting.objects.filter(is_opened=True).exists():
                setting = Setting.objects.get(is_opened=True)

                if user.groups.filter(id=settings.G_APPLICANT).exists():
                    if ((setting.submit_beg_time is not None) or (setting.submit_end_time is not None)) and not (
                            setting.submit_beg_time <= now <= setting.submit_end_time):
                        raise PermissionDenied("未到系统开放时间，请稍后再试！")
                elif user.groups.filter(id=settings.G_COLLEGE).exists():
                    if ((setting.submit_beg_time is not None) or (setting.submit_end_time is not None)) and not (
                            setting.submit_beg_time <= now <= setting.submit_end_time):
                        raise ValidationError(self.request, "未到系统开放时间，请稍后再试！")
                elif user.groups.filter(id=settings.G_PANELIST).exists():
                    if ((setting.review_beg_time is not None) or (setting.review_end_time is not None)) and not (
                            setting.review_beg_time <= now <= setting.review_end_time):
                        raise ValidationError(self.request, "未到系统开放时间，请稍后再试！")
            else:
                raise ValidationError('系统未开放，请稍后再试！', code='invalid_login')


class UserForm(UserCreationForm):
    username = forms.CharField(label='用户名', widget=UnfoldAdminTextInputWidget)
    password1 = forms.CharField(label='密码', widget=UnfoldAdminPasswordInput, help_text='密码至少8位')
    password2 = forms.CharField(label='确认密码', widget=UnfoldAdminPasswordInput, help_text='与密码一致')

    class Meta:
        model = User
        fields = ["username", 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    name = forms.CharField(label='姓名', widget=UnfoldAdminTextInputWidget)

    class Meta:
        model = User
        fields = ['name']


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='用户名', widget=UnfoldAdminTextInputWidget)
    email = forms.CharField(label='电子邮箱', widget=UnfoldAdminEmailInputWidget)
    password1 = forms.CharField(label='密码', widget=UnfoldAdminPasswordInput)
    password2 = forms.CharField(label='确认密码', widget=UnfoldAdminPasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if hasattr(self.instance, 'user'):
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise ValidationError("电子邮箱已存在，请重新输入")
        else:
            if User.objects.filter(email=email).exists():
                raise ValidationError("电子邮箱已存在，请重新输入")

        return email

    class Meta:
        model = User
        fields = ["username", "email", 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    name = forms.CharField(label='姓名', widget=UnfoldAdminTextInputWidget)
    gender = forms.ModelChoiceField(label='性别', queryset=Gender.objects.all(), widget=UnfoldAdminSelectWidget)
    idtype = forms.ModelChoiceField(label='证件类型', queryset=Idtype.objects.all(), widget=UnfoldAdminSelectWidget,
                                    initial=1)
    education = forms.ModelChoiceField(label='学历', queryset=Education.objects.all(), widget=UnfoldAdminSelectWidget)
    degree = forms.ModelChoiceField(label='学位', queryset=Degree.objects.all(), widget=UnfoldAdminSelectWidget)
    title = forms.ModelChoiceField(label='职称', queryset=Title.objects.all(), widget=UnfoldAdminSelectWidget)
    department = forms.ModelChoiceField(
        label="所属学院", queryset=Department.objects.filter(is_enable=True), widget=UnfoldAdminSelectWidget
    )
    idnumber = forms.CharField(label="证件号码", validators=[IDValidator], widget=UnfoldAdminTextInputWidget)
    phone = forms.CharField(label="联系电话", widget=UnfoldAdminTextInputWidget)

    # birthday = forms.DateField(label='出生日期', widget=UnfoldAdminSingleDateWidget)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit():
            raise ValidationError("手机号不是数字，请检查后重新输入")
        elif len(phone) != 11:
            raise ValidationError("手机号不是11位数字，请检查后重新输入")
        elif hasattr(self.instance, 'user'):
            if Profile.objects.filter(phone=phone).exclude(user_id=self.instance.user.id).exists():
                raise ValidationError("手机号已存在，请重新输入")
        else:
            if Profile.objects.filter(phone=phone).exists():
                raise ValidationError("手机号已存在，请重新输入")

        return phone

    class Meta:
        model = Profile
        fields = ['name', 'gender', 'department', 'phone', 'idtype', 'idnumber', 'education', 'degree',
                  'title']
