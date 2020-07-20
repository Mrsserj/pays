from django.contrib.auth.models import User
from rest_framework import serializers
from pays.models import TransferTransaction, FillUpTransaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['uid', 'amount']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    wallet = WalletSerializer(required=False)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'wallet']


class Transaction(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


class TransferSerializer(Transaction):
    class Meta:
        model = TransferTransaction
        fields = ['from_wallet', 'to_wallet', 'amount', 'owner']

    def create(self, validated_data):
        return TransferTransaction.objects.create(**validated_data)


class FillUpSerializer(Transaction):
    class Meta:
        model = FillUpTransaction
        fields = ['to_wallet', 'amount', 'owner']

    def create(self, validated_data):
        return FillUpTransaction.objects.create(**validated_data)