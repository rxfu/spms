from django import forms
from unfold.widgets import UnfoldAdminTextareaWidget, UnfoldBooleanSwitchWidget

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    opinion = forms.CharField(label='评审意见', widget=UnfoldAdminTextareaWidget)
    # is_agreed = forms.BooleanField(label='是否同意申报',
    #                                widget=UnfoldAdminRadioSelectWidget(radio_style=HORIZONTAL,
    #                                                                    choices=((0, '不同意'), (1, '同意'))),
    #                                required=False)
    is_agreed = forms.BooleanField(label='同意申报', widget=UnfoldBooleanSwitchWidget, required=False)

    class Meta:
        model = Review
        fields = ['opinion', 'is_agreed']
