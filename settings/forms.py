from django import forms
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget, UnfoldAdminSplitDateTimeWidget, \
    UnfoldBooleanSwitchWidget

from settings.models import Setting, Series, Phase


class SettingForm(forms.ModelForm):
    year = forms.CharField(label='年度', widget=UnfoldAdminTextInputWidget)
    series = forms.ModelChoiceField(label='项目系列', queryset=Series.objects.all(), widget=UnfoldAdminSelectWidget)
    phase = forms.ModelChoiceField(label='项目阶段', queryset=Phase.objects.all(), widget=UnfoldAdminSelectWidget)
    submit_beg_time = forms.SplitDateTimeField(label='开始提交时间', widget=UnfoldAdminSplitDateTimeWidget,
                                               required=False)
    submit_end_time = forms.SplitDateTimeField(label='结束提交时间', widget=UnfoldAdminSplitDateTimeWidget,
                                               required=False)
    review_beg_time = forms.SplitDateTimeField(label='开始评审时间', widget=UnfoldAdminSplitDateTimeWidget,
                                               required=False)
    review_end_time = forms.SplitDateTimeField(label='结束评审时间', widget=UnfoldAdminSplitDateTimeWidget,
                                               required=False)
    is_opened = forms.BooleanField(label='是否开启', widget=UnfoldBooleanSwitchWidget, required=False)

    class Meta:
        model = Setting
        fields = ['year', 'series', 'phase', 'submit_beg_time', 'submit_end_time', 'review_beg_time', 'review_end_time',
                  'is_opened']
