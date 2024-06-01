from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'user','name', 'currency', 'created_at', 'updated_at', 'is_active')
        read_only_fields = ('user', 'created_at', 'updated_at')
    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)
        
        # Remove the 'user' field from the representation
        representation.pop('user', None)
        
        return representation
    

# wallet serializer
class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)



class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    recipient_wallet_id = serializers.IntegerField()