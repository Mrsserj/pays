from django.db import models
from django.contrib.auth.models import User
import uuid


class OperationStatus:
    NEW = 0
    CANCEL = -1
    COMPLETE = 1


TRANSACTION_STATUS = (
    (OperationStatus.CANCEL, u'Отменена'),
    (OperationStatus.NEW, u'Новая'),
    (OperationStatus.COMPLETE, u'Проведена'),
)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    uid = models.UUIDField(primary_key=True, unique=True, editable=False,
                           default=uuid.uuid4)

    @property
    def amount(self):
        _sum = self.operation_set.all().aggregate(models.Sum('amount'))
        return _sum['amount__sum'] or 0.0


def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


models.signals.post_save.connect(create_wallet, sender=User)


class Operation(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    transaction = models.ForeignKey("Transaction", on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def delete(self, using=None, keep_parents=False):
        pass

    def save(self, *args, **kwargs):
        if not self.id:
            super(Operation, self).save()


class Transaction(models.Model):
    uid = models.UUIDField(primary_key=True, unique=True, editable=False,
                           default=uuid.uuid4)
    status = models.SmallIntegerField(default=OperationStatus.NEW,
                                      choices=TRANSACTION_STATUS)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    to_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def delete(self, using=None, keep_parents=False):
        pass

    def save(self, *args, **kwargs):
        pass


class TransferTransaction(Transaction):
    from_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.amount > self.from_wallet.amount:
            raise ValueError('insufficient funds')
        super(Transaction, self).save(*args, **kwargs)
        super(TransferTransaction, self).save(*args, **kwargs)
        _op_from = Operation.objects.create(
            wallet=self.from_wallet,
            transaction=self,
            amount=self.amount*-1
        )
        _op_to = Operation.objects.create(
            wallet=self.to_wallet,
            transaction=self,
            amount=self.amount
        )
        if _op_from and _op_to:
            _tr_status = OperationStatus.COMPLETE
        else:
            _tr_status = OperationStatus.CANCEL

        Transaction.objects.filter(pk=self.pk).update(
                status=_tr_status)

        return self.uid


class FillUpTransaction(Transaction):

    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)
        Operation.objects.create(
            wallet=self.to_wallet,
            transaction=self,
            amount=self.amount
        )
        return self.uid


def create_fillup(sender, instance, created, **kwargs):
    if created:
        FillUpTransaction.objects.create(to_wallet=instance, amount=100)


models.signals.post_save.connect(create_fillup, sender=Wallet)
