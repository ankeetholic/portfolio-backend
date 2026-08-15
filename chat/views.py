from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.huggingface import generate_chat_response

class ChatAPIView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Optional: rate limiting, simple validation could go here
        if len(message) > 500:
            return Response({"error": "Message is too long"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            response_data = generate_chat_response(message)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
