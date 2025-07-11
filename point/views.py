from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PointHistory


# Create your views here.

class PointHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        histories = PointHistory.objects.filter(user=user).order_by('-created_at')

        history_list = [
            {
                "amount": h.amount,
                "reason": h.get_reason_display(),
                "created_at": h.created_at.strftime("%Y.%m.%d")
            }
            for h in histories
        ]

        return Response({
            "point": user.point,
            "history": history_list
        })
