from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count,Sum
from django.db.models import Q
from django.db.models.functions import Coalesce
# Create your models here.

class Transaction(models.Model):
    CHARGE=1
    PURCHASE=2
    TRANSFER=3
    TRANSACTION_TYPE_MODEL=(
        (CHARGE,"charge"),
        (PURCHASE,"purchase"),
        (TRANSFER,"transfer"),
        
    )
    user=models.ForeignKey(User,related_name='transaction',on_delete=models.RESTRICT)
    transaction_type=models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE_MODEL,default=CHARGE)
    amount=models.BigIntegerField()
    created_time=models.DateTimeField(auto_now_add=True)
    
    
    
    
    def __str__(self):
        return f"{self.user}-{self.get_transaction_type_display()}-{self.amount}"
    
    
    # @classmethod
    # def get_report(cls):
    #     positive_transaction=Sum('transaction_amount',filter=(Q(transactions__transaction_type=1)))
        
    #     negative_transaction=sum('transaction_amount',filter=Q(transactions__transaction_type__in=[2,3]))
    #     # show all users and their balance
    #     user=User.objects.all().annotate(
    #         transaction_count=Count('transaction_id'),
    #         balance=positive_transaction - negative_transaction
    #         )    
    
        
    @classmethod
    def get_report(cls):
        positive_transaction=Sum('transaction__amount',filter=(Q(transaction__transaction_type=1)))
        negetive_transaction=Sum('transaction__amount',filter=(Q(transaction__transaction_type__in=[2,3])))

        users=User.objects.all().annotate(
            tr_count=Count('transaction__id'),
            balance=Coalesce(positive_transaction,0) - Coalesce(negetive_transaction,0) 
            )

        return users
        
        
        
    @classmethod
    def get_total_balance(cls,user):
        # User.objects.all().aggregate(
        #     transaction_count =Count('transaction__id'),
        #     total_balance=Sum('transaction__amount')
        # )
        queryset=cls.get_report()
        return queryset.aggregate(total_balance=Sum('balance'))
        
        
        
class UserBalance(models.Model):
    user=models.ForeignKey(User,related_name="balance_rekord",on_delete=models.RESTRICT)
    balance=models.BigIntegerField()
    created_time=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user}-{self.balance}-{self.created_time}"
