import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib import messages
from Extentions.utils import get_random_code, write_action
from .models import User, LoginCodeModel
from .forms import SignUpForm, SignInForm, EnterCodePWForm
from .decorators import login_not_required
# imports for activatings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token


# url: /sign-up
@login_not_required
def sign_up_page(request):
	form = SignUpForm(request.POST or None)
	context = {'form': form}

	if form.is_valid():
		user = form.save(commit=False)
		user.is_active = True
		user.save()

		if user:
			login_code = LoginCodeModel.objects.create(
				user=user,
				is_use=False
			)
			# set password for user
			user.set_password(str(login_code.code))
			user.save()

			print(str(login_code.code)) #TODO

			write_action(f'{user.username} - Created Account')
			uid = urlsafe_base64_encode(force_bytes(user.pk))
			token = account_activation_token.make_token(user)
			messages.success(request, _('حساب کاربری شما با موفقیت ایجاد شد. برای ورود کد پیامک شده را وارد کنید'))
			return redirect(f'/{get_language()}/enter-sms-code/{uid}/{token}')

		messages.error(request, _('مشکلی بوجود آمده است'))
		return redirect('/sign-up')
	return render(request, 'ampool_auth/signup.html', context)


# url: /sign-in
@login_not_required
def sign_in_page(request):
	form = SignInForm(request.POST or None)
	context = {'form': form}

	if form.is_valid():
		phone = form.cleaned_data.get('phone')
		find_user = User.objects.filter(phone=phone).first()

		if find_user:

			login_code = LoginCodeModel.objects.create(
				user=find_user,
				is_use=False
			)
			if login_code:
				find_user.set_password(str(login_code.code))
				find_user.save()

			print(str(login_code.code)) #TODO

			context['form'] = SignInForm()
			uid = urlsafe_base64_encode(force_bytes(find_user.pk))
			token = account_activation_token.make_token(find_user)
			messages.success(request, _('پیامک حاوی کد برای شما ارسال شد. بعد از دریافت کد، آن را وارد کنید'))
			return redirect(f'/{get_language()}/enter-sms-code/{uid}/{token}')

		messages.error(request, _('شماره تلفن شما اشتباه است و یا در سیستم موجود نیست'))
		return redirect('/sign-in')
	
	return render(request, 'ampool_auth/signin.html', context)


# url: /enter-sms-code/<uidb64>/<token>
@login_not_required
def enter_sms_code(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user and account_activation_token.check_token(user, token):
		form = EnterCodePWForm(request.POST or None)
		context = {'form': form}

		if form.is_valid():
			code = form.cleaned_data.get('code')
			pw_code = LoginCodeModel.objects.filter(
				user=user, 
				code=code, 
				expire_date__gt=datetime.datetime.now(), 
				is_use=False
			).first()

			if pw_code:
				user = authenticate(username=user.username, password=code)
				if user:
					# set is_use for password
					pw_code.is_use = True
					pw_code.save()
					
					# check is_active of user
					if not user.is_active:
						user.is_active = True
						user.save()

					login(request, user)
					write_action(f'{user.username} - Signed In to WebSite!')

					context['form'] = EnterCodePWForm()
					messages.success(request, _('به آمپول خوش آمدید'))
					return redirect('/')
				else:
					messages.error(request, _('مشکلی در ورود شما بوجود آمد'))
					return redirect('auth:signin')
			else:
				messages.error(request, _('کد شما نامعتبر و یا منقضی شده است'))
				return redirect('auth:signin')

		return render(request, 'ampool_auth/enter_code.html', context)


# url: /sign-out
@login_required
def sign_out_page(request):
	logout(request)
	messages.info(request, _('شما با موفقیت خارج شدید'))
	return redirect('/sign-in')