from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from exchange.iota import IOTA
from exchange.models import Coin, WithdrawalRequest
from user.models import User


class Command(BaseCommand):

    help = "Check if there's anything in Hub that needs to be processed"

    def handle(self, *args, **options):

        api = IOTA()
        coin = Coin.objects.by_symbol('MIOTA')
        since = coin.last_hub_check

        print(since)

        data = api.get_active_balances(since)
        
        if data and api.batch_to_exchange(data):
            for user_id, balance in data.items():
                user = User.objects.get(id=user_id.split('-')[1])
                user.alter_balance('MIOTA', int(balance), modification_type='DEPOSIT')
                print("Gave %d iota to user %s after deposit" % (int(balance), user_id))

        coin.last_hub_check = timezone.now()
        coin.save()


        for wr in WithdrawalRequest.objects.filter(processed=False, coin=coin):
            status = api.withdraw('exchange', int(wr.amount), wr.address, validate_checksum=True, tag='FAKEXCHANGE')

            if not status:
                print("Failed to withdraw")
                wr.failed = True
                wr.save()
            else:
                wr.processed = True
                wr.processed_at = timezone.now()
                wr.comment = status
                wr.save()

                
