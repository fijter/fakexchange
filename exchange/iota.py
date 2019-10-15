import requests
import datetime

class IOTA(object):

    def __init__(self):
        self.api_address = 'http://127.0.0.1:8888'

    def request(self, payload):
        headers = {'Content-Type': 'application/json', 'X-IOTA-API-Version': '1'}
        response = requests.post(self.api_address, json=payload, headers=headers)
        
        print(payload)

        if not response.ok:
            raise ValueError('Invalid response', '%s: %s' % (response.status_code, response))

        return response.json()

    def check_address(self, address, validate_checksum=True):
        ret = self.request({'command': 'WasAddressSpentFrom', 'address': address, 'validateChecksum': validate_checksum})

        if ret.get('wasAddressSpentFrom') == 'false':
            return True
        return False

    def create_user(self, user_id):
        ret = self.request({'command': 'CreateUser', 'userId': 'user-%s' % user_id})
        if 'error' in ret:
            return False
        else:
            return True
        
    def get_deposit_address(self, user_id):
        self.create_user(user_id)
        ret = self.request({'command': 'GetDepositAddress', 'userId': 'user-%s' % user_id})
        if 'address' in ret:
            return ret['address']

        return False


    def withdraw(self, user_id, amount, address, validate_checksum=True, tag='FAKEXCHANGE'):
        self.create_user(user_id)
        ret = self.request({
            'command': 'UserWithdraw', 
            'userId': 'user-%s' % user_id, 
            'amount': amount,
            'payoutAddress': address,
            'validateChecksum': validate_checksum,
            'tag': tag
        })
        
        if 'uuid' in ret:
            return ret['uuid']
        else:
            return False

    def check_balance(self, user_id):
        self.create_user(user_id)
        ret = self.request({'command': 'GetBalance', 'userId': 'user-%s' % user_id})
        return ret.get('available')

    def get_balance_changes(self, since=None):
        if since:
            since = since.strftime('%s000')
        else:
            since = 0

        ret = self.request({'command': 'BalanceSubscription', 'newerThan': since})
        return ret

    def active_users(self, since=None):
        balance_changes = self.get_balance_changes(since=since)
        active_users = set()
        for event in balance_changes.values():
            u = event.get('userId')
            if u:
                active_users.add(u)
        return active_users

    def get_active_balances(self, since=None):
        users = self.active_users(since=since)
        ubalance = {}
        for user in users:
            ubalance[user] = self.check_balance(user.split('-', 1)[1])

        return ubalance

    def batch_to_exchange(self, batch):
        self.create_user('exchange')
        newbatch = []
        to_exchange = 0

        for user_id, amount in batch.items():
            newbatch.append({'userId': user_id, 'amount': 0-int(amount)})
            to_exchange += int(amount)

        newbatch.append({'userId': 'user-exchange', 'amount': to_exchange})

        ret = self.request({'command': 'ProcessTransferBatch', 'transfers': newbatch})
        
        if not 'error' in ret:
            return True
        else:
            print(ret['error'])
            return False

    def exchange_to_user(self, amount, user_id):

        newbatch = []

        newbatch.append({'userId': user_id, 'amount': int(amount)})
        newbatch.append({'userId': 'user-exchange', 'amount': 0-int(amount)})

        ret = self.request({'command': 'ProcessTransferBatch', 'transfers': newbatch})
        
        if not 'error' in ret:
            return True
        else:
            print(ret['error'])
            return False
        
