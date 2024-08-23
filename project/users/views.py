from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic

COST_PER_KM = 5.0

@api_view(['POST'])
def calculate_delivery_cost(request):
    try:

        coordinates = {
            'latitude_a': request.data.get('latitude_a'),
            'longitude_a': request.data.get('longitude_a'),
            'latitude_b': request.data.get('latitude_b'),
            'longitude_b': request.data.get('longitude_b')
        }


        for key, value in coordinates.items():
            if not value:
                raise ValueError(f"Missing {key} coordinate")
            try:
                coordinates[key] = float(value)
            except ValueError:
                raise ValueError(f"Invalid {key} coordinate")


        point_a = (coordinates['latitude_a'], coordinates['longitude_a'])
        point_b = (coordinates['latitude_b'], coordinates['longitude_b'])
        distance_km = round(geodesic(point_a, point_b).kilometers, 6)
        total_cost_usd = round(distance_km * COST_PER_KM, 2)


        return Response({
            'distance_km': distance_km,
            'total_cost_usd': total_cost_usd
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)