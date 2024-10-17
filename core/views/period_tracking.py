from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime, timedelta
from core.models import PeriodLog
from core.serializers import PeriodLogSerializer

class PeriodTrackingViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PeriodLog.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def predict_next(self, request):
        # Get last 3 cycles to calculate average
        last_periods = self.get_queryset().order_by('-start_date')[:3]
        if len(last_periods) < 2:
            return Response({
                "message": "Need more data for prediction",
                "prediction": None
            })

        # Calculate average cycle length
        cycle_lengths = []
        for i in range(len(last_periods)-1):
            delta = last_periods[i].start_date - last_periods[i+1].start_date
            cycle_lengths.append(delta.days)

        avg_cycle = sum(cycle_lengths) / len(cycle_lengths)
        last_start = last_periods[0].start_date
        predicted_date = last_start + timedelta(days=round(avg_cycle))

        return Response({
            "message": "Prediction based on your last cycles",
            "prediction": predicted_date
        })