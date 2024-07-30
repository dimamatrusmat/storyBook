from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .forms import RegistretionForm
from .tokens import account_activation_token


def account_register(request):

    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        registerForm = RegistretionForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('users/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),

            })
            user.email_user(subject=subject, message=message)

    else:
        registerForm = RegistretionForm()
    return render(request, 'users/registration/register.html', {'form': registerForm})
