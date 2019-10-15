from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def balance(self, symbol):
        from exchange.models import UserBalance, Coin
        coin = Coin.objects.by_symbol(symbol)
        balance, created = UserBalance.objects.get_or_create(user=self, coin=coin, defaults={'balance': 0})
        return balance

    def all_balances(self):
        from exchange.models import UserBalance, Coin
        balances = {}
        for coin in Coin.objects.all():
            balances[coin] = self.balance(coin.symbol)
        return balances

    def full_history(self):
        return self.history.all()
    
    def withdraw(self, symbol, amount, payment_address):
        from exchange.models import WithdrawalRequest, Coin
        # We don't allow withdrawals larger as the balance
        if self.balance(symbol).balance < amount:
            return (False, 'Insufficient balance')

        coin = Coin.objects.by_symbol(symbol)

        # Check if the address is a valid address to deposit to
        success, error = coin.check_withdrawal_address(payment_address)
        if not success:
            return (False, error)

        WithdrawalRequest(user=self, coin=coin, amount=amount, address=payment_address).save()
        self.alter_balance(symbol, 0-amount, 'WITHDRAWAL', modified_by=self, payment_address=payment_address)
        return (True, None)
    
    def deposit(self, symbol, amount, payment_address):
        self.alter_balance(symbol, amount, 'DEPOSIT', modified_by=self, payment_address=payment_address)

    def deposit_address(self, symbol):
        '''
        Returns a new deposit address for our given symbol
        '''

        if symbol in ('IOTA', 'MIOTA'):
            from exchange.iota import IOTA
            api = IOTA()
            addr = api.get_deposit_address(self.id)
            if not addr:
                return 'Unable to generate'
            else:
                return addr
        
        if symbol == 'BTC':
            return '1CFBdvaiZgZPTZERqnezAtDQJuGHKoHSzg'

    def alter_balance(self, symbol, amount, modification_type='MANUAL', modified_by=None, payment_address=None):
        '''
        Alter the balance of a symbol for a user
        Keeps track of history for us, we always use this method
        for altering the balance.
        '''

        from exchange.models import UserBalance, Coin, BalanceHistory
        
        coin = Coin.objects.by_symbol(symbol)
        balance, created = UserBalance.objects.get_or_create(user=self, coin=coin, defaults={'balance': 0})
        balance.balance += amount
        balance.save()

        BalanceHistory(
            user=self, 
            coin=coin, 
            amount=amount, 
            modification_type=modification_type, 
            modified_by_user=modified_by, 
            payment_address=payment_address
        ).save()
