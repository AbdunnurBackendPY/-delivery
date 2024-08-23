from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic

COST_PER_KM = 5

@api_view(['POST'])
def calculate_delivery_cost(request):
    try:
        # Extract coordinates from request data
        coordinates = {
            'latitude_a': request.data.get('latitude_a'),
            'longitude_a': request.data.get('longitude_a'),
            'latitude_b': request.data.get('latitude_b'),
            'longitude_b': request.data.get('longitude_b')
        }

        # Validate coordinates
        for key, value in coordinates.items():
            if not value:
                raise ValueError(f"Missing {key} coordinate")
            try:
                coordinates[key] = float(value)
            except ValueError:
                raise ValueError(f"Invalid {key} coordinate")

        # Calculate distance and cost
        point_a = (coordinates['latitude_a'], coordinates['longitude_a'])
        point_b = (coordinates['latitude_b'], coordinates['longitude_b'])
        distance_km = geodesic(point_a, point_b).kilometers
        total_cost_usd = distance_km * COST_PER_KM

        # Return response
        return Response({
            'distance_km': round(distance_km, 2),
            'total_cost_usd': round(total_cost_usd, 2)
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)