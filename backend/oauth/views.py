from rest_framework import serializers
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, inline_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AuthEmailSerializer, AuthUsernameSerializer


@extend_schema_view(
    post=extend_schema(
        parameters=[OpenApiParameter(
            'by', str,
            enum=['email', 'username'],
            default='email'
        )],
        request=inline_serializer('auth_request', {
            'email': serializers.CharField(),
            # 'passport_series': serializers.CharField(),
            # 'passport_number': serializers.CharField(),
            'username': serializers.CharField(),
            'password': serializers.CharField()
        }),
        responses={
            '200': inline_serializer('auth_response2', {
                'access': serializers.CharField(),
                'refresh': serializers.CharField()
            })
        }
    )
)
class AuthView(TokenObtainPairView):

    def get_serializer_class(self):
        return AuthUsernameSerializer if self.request.query_params.get("by", "email") == "username" else AuthEmailSerializer

