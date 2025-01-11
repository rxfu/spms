from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget, UnfoldAdminSingleDateWidget

from projects.models import Information, Member
from settings.models import Type, Subject, Gender, Education, Degree, Title, Department


class MemberInlineForm(forms.ModelForm):
    name = forms.CharField(label='姓名', widget=UnfoldAdminTextInputWidget)
    gender = forms.ModelChoiceField(label='性别', queryset=Gender.objects.all(), widget=UnfoldAdminSelectWidget)
    education = forms.ModelChoiceField(label='学历', queryset=Education.objects.all(), widget=UnfoldAdminSelectWidget)
    degree = forms.ModelChoiceField(label='学位', queryset=Degree.objects.all(), widget=UnfoldAdminSelectWidget)
    title = forms.ModelChoiceField(label='职称', queryset=Title.objects.all(), widget=UnfoldAdminSelectWidget)
    department = forms.ModelChoiceField(
        label="所属学院", queryset=Department.objects.filter(is_enable=True), widget=UnfoldAdminSelectWidget
    )
    phone = forms.CharField(label="联系电话", widget=UnfoldAdminTextInputWidget)
    subject = forms.ModelChoiceField(label='所属学科', queryset=Subject.objects.all(), widget=UnfoldAdminSelectWidget)
    area = forms.CharField(label='研究领域', widget=UnfoldAdminTextInputWidget)

    class Meta:
        model = Member
        fields = ['name', 'gender', 'education', 'degree', 'title', 'department', 'phone', 'subject', 'area']


class InformationForm(forms.ModelForm):
    name = forms.CharField(label='项目名称', widget=UnfoldAdminTextInputWidget)
    beg_year = forms.DateField(label='项目起始年月', widget=UnfoldAdminSingleDateWidget())
    end_year = forms.DateField(label='项目结束年月', widget=UnfoldAdminSingleDateWidget())
    type = forms.ModelChoiceField(label='项目研究类型', queryset=Type.objects.all(), widget=UnfoldAdminSelectWidget)
    subject = forms.ModelChoiceField(label='所属学科', queryset=Subject.objects.all(), widget=UnfoldAdminSelectWidget)
    direction = forms.CharField(label='研究方向', widget=UnfoldAdminTextInputWidget, required=False)
    purpose = forms.CharField(label='研究目的和意义', widget=CKEditorUploadingWidget, required=False)
    content = forms.CharField(label='研究内容', widget=CKEditorUploadingWidget, required=False)
    progress = forms.CharField(label='研究进度', widget=CKEditorUploadingWidget, required=False)
    result = forms.CharField(label='预期成果', widget=CKEditorUploadingWidget, required=False)
    budget = forms.CharField(label='经费预算', widget=CKEditorUploadingWidget, required=False)

    # application_attachment = forms.FileField(label='项目申请书', widget=UnfoldAdminFileFieldWidget, required=False)

    class Meta:
        model = Information
        fields = ['name', 'beg_year', 'end_year', 'type', 'subject', 'direction', 'purpose', 'content', 'progress',
                  'result', 'budget']
