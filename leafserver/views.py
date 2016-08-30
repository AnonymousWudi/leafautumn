# coding=utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View

from forms import LoginForm


# Create your views here.
class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        user = request.user
        redirect_url = request.GET.get('next_start', '/index/')
        form = LoginForm()

        if user.is_authenticated():
            return redirect(redirect_url)

        ret = {
            'form': form,
            'redirect_url': redirect_url
        }
        return render(request, self.template_name, ret)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_ajax = request.POST.get('is_ajax', False)
        redirect_url = request.REQUEST.get('redirect_url', '/index/')

        if request.user.is_authenticated():
            return redirect(redirect_url)

        form = LoginForm(request.POST)
        if form.login(request):
            if is_ajax:
                return JsonResponse({'success': True, 'redirect_url': redirect_url})
            else:
                return redirect(redirect_url)
        else:
            if is_ajax:
                return JsonResponse({'success': False})

        ret = {
            'form': form,
            'redirect_url': redirect_url
        }
        return render(request, self.template_name, ret)


class DashboardView(View):
    template_name = 'dashboard.html'
