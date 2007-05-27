

from esp.users.models import ESPUser, User, UserBit
from esp.users.forms.user_reg import UserRegForm, EmailUserForm
from esp.web.util.main import render_to_response
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect

__all__ = ['join_emaillist','user_registration']

def join_emaillist(request):
    """
    View to join our email list.
    """

    if request.user.is_authenticated():
        return render_to_response('registration/already_logged_in.html',
                                  request, request.get_node('Q/Web/myesp'), {})


    if request.method == 'POST':
        form = EmailUserForm(request.POST)


        if form.is_valid():
            # create the user
            User.objects.get_or_create(email    = form.clean_data['email'],
                                       username = form.clean_data['email'],
                                       password = 'emailuser')
            return HttpResponseRedirect('/')
    else:
        form = EmailUserForm()

    return render_to_response('registration/emailuser.html',
                              request, request.get_node('Q/Web/myesp'), {'form':form})

            

def user_registration(request):
    """
    Registration view -- takes care of users who want to create a
    new account.
    """

    if request.user.is_authenticated():
        return render_to_response('registration/already_logged_in.html',
                                  request, request.get_node('Q/Web/myesp'), {})

    if request.method == 'POST':
        form = UserRegForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(email=form.clean_data['email'],
                                        password = 'emailuser')
            except User.DoesNotExist:
                user = User(email = form.clean_data['email'])

            user.username   = form.clean_data['username']
            user.last_name  = form.clean_data['last_name']
            user.first_name = form.clean_data['first_name']

            user.set_password(form.clean_data['password'])

            user.save()

            role_verb = request.get_node('V/Flags/UserRole/%s' % form.clean_data['initial_role'])

            role_bit  = UserBit.objects.create(user = user,
                                               verb = role_verb,
                                               qsc  = request.get_node('Q'),
                                               recursive = False)

            user = authenticate(username=form.clean_data['username'],
                                password=form.clean_data['password'])

            login(request, user)

            return HttpResponseRedirect('/myesp/profile/')
    else:
        form = UserRegForm()

    return render_to_response('registration/newuser.html',
                              request, request.get_node('Q/Web/myesp'),{'form':form})




