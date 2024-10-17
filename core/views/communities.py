from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Community, CommunityMembership
from core.serializers import CommunitySerializer, CommunityMembershipSerializer

class CommunityViewSet(viewsets.ModelViewSet):
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Community.objects.all()

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        community = self.get_object()
        membership, created = CommunityMembership.objects.get_or_create(
            user=request.user,
            community=community,
            defaults={'role': 'member'}
        )
        return Response(status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)