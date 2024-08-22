from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic

COST_PER_KM = 5


@api_view(['POST'])
def calculate_delivery_cost(request):
    try:
        latitude_a = float(request.data.get('latitude_a'))
        longitude_a = float(request.data.get('longitude_a'))
        latitude_b = float(request.data.get('latitude_b'))
        longitude_b = float(request.data.get('longitude_b'))

        point_a = (latitude_a, longitude_a)
        point_b = (latitude_b, longitude_b)

        distance = geodesic(point_a, point_b).kilometers
        total_cost = distance * COST_PER_KM

        return Response({
            'distance_km': round(distance, 2),
            'total_cost_usd': round(total_cost, 2)
        }, status=status.HTTP_200_OK)

    except (TypeError, ValueError, KeyError):
        return Response(
            {'error': 'Неверные или отсутствующие данные'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
