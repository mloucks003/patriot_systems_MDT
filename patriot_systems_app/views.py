from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle
from django.db.models.functions import Upper, Trim
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def plate_check(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            logger.info(f"Received data: {data}")  # Log the received data

            # Try to get the license plate number from both possible parameters
            plate_number = data['queryResult']['parameters'].get('licensePlate') or data['queryResult']['parameters'].get('plateNumber')
            if not plate_number:
                return JsonResponse({'fulfillmentText': 'No license plate number was provided.'}, status=400)

            logger.info(f"Looking up plate number: '{plate_number}'")

            try:
                # Normalize the plate number for case-insensitive and trimmed comparison
                normalized_plate_number = plate_number.strip().upper()
                vehicle = Vehicle.objects.get(license_plate__iexact=normalized_plate_number)
                
                owner = vehicle.owner
                # Create a natural language response
                response_text = (
                    f"10 4, the vehicle with license plate {plate_number} is a {vehicle.year} {vehicle.make} {vehicle.model}, "
                    f"color {vehicle.color}. The insurance is {'valid' if vehicle.is_insurance_valid else 'not valid'} and the registration is "
                    f"{'valid' if vehicle.is_registration_valid else 'not valid'}. The owner is {owner.name}, residing at {owner.address}."
                )
                response_data = {
                    "fulfillmentText": response_text
                }
            except Vehicle.DoesNotExist:
                logger.info("No vehicle found for plate number: " + plate_number)
                response_data = {"fulfillmentText": "No information found for that license plate."}

            return JsonResponse(response_data)
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON data")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError:
            logger.error("Missing required parameters")
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
    
    return JsonResponse({'error': 'This endpoint supports only POST requests'}, status=405)
