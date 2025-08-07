from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from django.db.models import Count

from .models import Vote
from .serializers import VoteSerializer, VoteResultSerializer
from .throttles import OncePerDayUserThrottle


class VoteCreateView(APIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [OncePerDayUserThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteResultsView(APIView):
    serializer_class_old_version = VoteSerializer  # for old application version
    serializer_class = VoteResultSerializer # for new application version
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        build_version = request.headers.get('X-Build-Version', '1.0')

        if user.restaurant:
            if build_version < '2.0':
                votes = Vote.objects.filter(
                    vote_date=today,
                    menu_item__menu__restaurant=user.restaurant,
                )
                serializer = self.serializer_class_old_version(votes, many=True)

            else:
                votes = Vote.objects.filter(
                    vote_date=today,
                    menu_item__menu__restaurant=user.restaurant
                ).values('menu_item').annotate(vote_count=Count('menu_item')).order_by('vote_count')
                serializer = self.serializer_class(votes, many=True, context={'request': request})

        else:
            return Response(
                {"error": "User must be associated with a restaurant"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
