from rest_framework import generics, permissions,status
from .models import Wallet
from .serializers import WalletBalanceSerializer, WalletSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TransferSerializer

class WalletListCreateAPIView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WalletDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

class WalletBalanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WalletBalanceSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            recipient_wallet_id = serializer.validated_data['recipient_wallet_id']
            
            # Get the sender's wallet
            sender_wallet = Wallet.objects.get(user=request.user)
            
            if sender_wallet.balance < amount:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the recipient's wallet
            try:
                recipient_wallet = Wallet.objects.get(id=recipient_wallet_id)
            except Wallet.DoesNotExist:
                return Response({"error": "Recipient wallet not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Perform the transfer
            sender_wallet.balance -= amount
            recipient_wallet.balance += amount
            sender_wallet.save()
            recipient_wallet.save()
            
            return Response({"success": "Transfer completed"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
