from django.utils.http import is_safe_url
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from authentication.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class UserPermissionRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        if not (
            request.user.is_admin or request.user == user or
            (
                request.user.has_perm("branch_manager") and
                request.user.branch == user.branch
            )
        ):
            return HttpResponseRedirect(reverse('micro_admin:userslist'))
        return super(UserPermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)



class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "/"
    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
                return redirect_path
        return self.default_next