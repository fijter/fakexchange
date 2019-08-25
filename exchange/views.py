from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal
from .models import Coin


class HomepageView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['section'] = 'home'
        return context


class DepositView(TemplateView):
    template_name = 'deposit.html'
    
    def get_context_data(self, **kwargs):
        context = super(DepositView, self).get_context_data(**kwargs)
        context['section'] = 'deposit'
        return context


class DepositAddressView(TemplateView):
    template_name = 'deposit_address.html'
    
    def get_context_data(self, **kwargs):
        context = super(DepositAddressView, self).get_context_data(**kwargs)
        context['section'] = 'deposit'
        context['coin'] = Coin.objects.by_symbol(kwargs['symbol'])
        context['address'] = self.request.user.deposit_address(kwargs['symbol'])
        return context


class WithdrawView(TemplateView):
    template_name = 'withdraw.html'
    
    def post(self, request, *args, **kwargs):
        coin = request.POST.get('symbol')
        to_withdraw = Decimal(request.POST.get('to_withdraw'))
        addr = request.POST.get('addr')

        success, error = request.user.withdraw(coin, to_withdraw, addr)

        if success:
            return HttpResponseRedirect('%s?success=1' % reverse('withdraw'))
        else:
            return HttpResponseRedirect('%s?error=%s' % (reverse('withdraw'), error))
            

    def get_context_data(self, **kwargs):
        context = super(WithdrawView, self).get_context_data(**kwargs)
        context['section'] = 'withdraw'
        return context


class HistoryView(TemplateView):
    template_name = 'history.html'
    
    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['section'] = 'history'
        return context
