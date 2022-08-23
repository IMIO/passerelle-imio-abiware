import requests
from django.db import models
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint


class ConnectorAbiware(BaseResource):
    """
    Connector Abiware
    """

    server_url_auth = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="URL du serveur d'authentification",
        help_text="URL du serveur ou le token OAuth2 sera pris",
    )

    client_id = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Client ID",
        help_text="Client ID pour la connexion OAuth2"
    )

    username = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Username",
        help_text="Username pour la connexion OAuth2",
    )

    password = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Mot de passe",
        help_text="Mot de passe pour la connexion OAuth2",
    )

    class Meta:
        verbose_name = "Connecteur pour la plateforme Abiware"

    @endpoint(
        name="get-token",
        perm="can_access",
        description="Get token",
        long_description="Obtenir le token d'identification OAuth2 via un post.",
        display_order=0,
        display_category="Test",
    )
    def get_token(self, request):
        url = str(self.server_url_auth)
        client_id = self.client_id
        username = self.username
        password = self.password
        return requests.post(
            url=url,
            data={
                "grant_type": "password",
                "client_id": client_id,
                "username": username,
                "password": password
            }
        )
