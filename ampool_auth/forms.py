import re
from django import forms
from .models import User
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from Extentions.utils import is_phone


class SignUpForm(forms.ModelForm):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))
    gender = forms.ChoiceField(
        choices=GENDER_USER, 
        widget=forms.RadioSelect(attrs={'name': 'gender_radio', 'checked': 'checked'})
    )
    # captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'gender']
        widgets = {
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'phone': forms.NumberInput({'placeholder': _('شماره تلفن خود را وارد کنید')}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(_('نام خود را وارد کنید'))
        for i in first_name:
            if ord(i) < 1000:
                raise forms.ValidationError(_('نام باید شامل کاراکترهای فارسی باشد'))
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(_('نام‌خانوادگی خود را وارد کنید'))
        for i in last_name:
            if ord(i) < 1000:
                raise forms.ValidationError(_(' نام‌خانوادگی باید شامل کاراکترهای فارسی باشد'))
        return last_name
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید'))
        is_phonee = is_phone(phone)
        if User.objects.filter(phone=phone).first():
            raise forms.ValidationError(_('این شماره تلفن در سیستم ثبت شده است'))
        if not is_phonee:
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        for i in str(phone):
            if ord(i) > 1000:
                raise forms.ValidationError(_('شماره تلفن باید شامل اعداد انگلیسی باشد'))
        return phone

class SignInForm(forms.Form):
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': _('شماره تلفن خود را وارد کنید') }))
    # captcha = CaptchaField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError(_('شماره تلفن همراه خود را وارد کنید'))

        is_phonee = is_phone(phone)
        
        if not User.objects.filter(phone=phone).first():
            raise forms.ValidationError(_('این شماره تلفن در سیستم موجود نیست'))
        if not is_phonee:
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        for i in str(phone):
            if ord(i) > 1000:
                raise forms.ValidationError(_('شماره تلفن باید شامل اعداد انگلیسی باشد'))
        return phone


class EnterCodePWForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': _('مانند: 12345')}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        is_code = bool(re.compile(r'[0-9]{5}').match(str(code)))
        
        if not is_code:
            raise forms.ValidationError(_('فرمت کد قابل قبول نیست'))
        for i in str(code):
            if ord(i) > 1000:
                raise forms.ValidationError(_('کد باید شامل اعداد انگلیسی باشد'))
        return code
