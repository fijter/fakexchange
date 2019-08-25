from django.db import models
import re


MODIFICATION_TYPES = (
    ('MANUAL', 'Manual modification by staff'),
    ('DEPOSIT', 'Deposit'),
    ('WITHDRAWAL', 'Withdrawal'),
)


class CoinManager(models.Manager):
    def by_symbol(self, symbol):
        return self.get(symbol=symbol)


class Coin(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    price_in_usd = models.DecimalField(max_digits=18, decimal_places=10)

    def __str__(self):
        return self.symbol   

    def check_withdrawal_address(self, addr):
        
        if self.symbol == 'BTC':
            expression = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
            if re.match(expression, addr):
                return (True, None)
            else:
                return (False, "Invalid address")

        if self.symbol in ('MIOTA', 'IOTA'):
            
            # We want to check 3 things with IOTA
            # First we want to check if the address is a valid address with checksum
            # Next up we want to check if the checksum is valid
            # Next up we want to make sure the address hasn't been spent from yet

            expression = r'^[A-Z9]{90}$'
            expression_nochecksum = r'^[A-Z9]{81}$'

            if re.match(expression, addr):
                # The next 4 lines are a quirky workaround for the Python IOTA library in Python 3.7
                # Needs to be resolved in that library first
                try:
                    import iota
                except:
                    pass

                # Check the checksum using one of the IOTA Client libraries
                from iota.types import Address
                if not Address(addr).is_checksum_valid():
                    return (False, "Invalid address, checksum not correct")

                return (True, None)

            else:
                if re.match(expression_nochecksum, addr):
                    return (False, "Please provide an address including a checksum")

            return (False, "Invalid address")
                

        return (False, "Unknown Symbol (%s), please contact support" % self.symbol)


    objects = CoinManager()


class UserBalance(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.PROTECT)
    coin = models.ForeignKey('exchange.Coin', on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=24, decimal_places=10, default=0)

    def __str__(self):
        return '%s %s -> %s' % (self.balance, self.coin.symbol, self.user.username)

    def save(self, *args, **kwargs):
        if 'non_manual' in kwargs:
            non_manual = kwargs.pop('non_manual')
            if non_manual:
                return super(UserBalance, self).save(*args, **kwargs)
        try:
            ub = UserBalance.objects.get(user=self.user, coin=self.coin)
            balance = ub.balance
        except UserBalance.DoesNotExist:
            balance = 0

        BalanceHistory(user=self.user, coin=self.coin, amount=self.balance - balance, modification_type='MANUAL').save()
        return super(UserBalance, self).save(*args, **kwargs)


    class Meta:
        unique_together = (('user', 'coin'),)


class WithdrawalRequest(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='withdrawals')
    coin = models.ForeignKey('exchange.Coin', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=24, decimal_places=10, default=0)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    failed = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return '%s -> %s -> %s' % (self.user, self.coin, self.amount)


class BalanceHistory(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='history')
    coin = models.ForeignKey('exchange.Coin', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=24, decimal_places=10, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modification_type = models.CharField(max_length=50, choices=MODIFICATION_TYPES)
    payment_address = models.CharField(max_length=255, null=True, blank=True)
    modified_by_user = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.PROTECT, related_name='modified_balance_history')

    def readable_type(self):
        return dict(MODIFICATION_TYPES)[self.modification_type]

    def __str__(self):
        return '%s -> %s -> %s' % (self.user, self.coin, self.amount)
