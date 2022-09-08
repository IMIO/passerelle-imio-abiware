import requests
from django.db import models
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint


class ConnectorAbiware(BaseResource):
    """
    Connector Abiware
    """

    server_url_auth = models.URLField(
        blank=False,
        verbose_name="URL du serveur d'authentification",
        help_text="URL du serveur ou le token OAuth2 sera pris",
    )

    server_api_url = models.URLField(
        verbose_name="URL de l'api Dossier d'AbiWare",
        help_text="URL de l'api d'AbiWare avec un / à la fin",
        blank=False,
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
        display_category="Token",
    )
    def get_token_endpoint(self, request):
        return self.get_token()

    def get_token(self):
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
        ).json()

    @endpoint(
        name="dossier",
        perm="can-access",
        methods=["post"],
        description="Créer un nouveau dossier",
        long_description="Permet de créer un nouveau dossier dans Abiware",
        display_category="Dossier",
        example_pattern="create",
        pattern="^create$",
    )
    def create_dossier_abiware(self, request):
        def check_params(params, index):
            if params[index] != "":
                return True
            else:
                return False

        token = self.get_token()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }

        server_api_url = "https://testdossierconnector.abicloud.be/api/"
        url = f"{server_api_url}dossiers/request"

        general_fields = ("partnerExternalId", "dossierExternalId", "zoneExternalId", "dossierCode")
        dossier_fields = ("dossier_data",)
        user_request_fields = ("user_request",)
        contacts_fields = ("contact_contact", "contact_demandeur", "contact_facturation", "contact_proprietaire")

        post_data = json.loads(request.body)

        general = {key: value for key, value in post_data.items() if key in general_fields}

        dossier_data = {key: value for key, value in post_data.items() if key in dossier_fields}
        dossier_data_split = dossier_data[dossier_fields[0]].split(" || ")
        dossier = {}
        if check_params(dossier_data_split, 0):
            dossier["name"] = dossier_data_split[0]
        if check_params(dossier_data_split, 1):
            dossier["street"] = dossier_data_split[1]
        if check_params(dossier_data_split, 2):
            dossier["houseNumber"] = dossier_data_split[2]
        if check_params(dossier_data_split, 3):
            dossier["poBoxNumber"] = dossier_data_split[3]
        if check_params(dossier_data_split, 4):
            dossier["zipCode"] = dossier_data_split[4]
        if check_params(dossier_data_split, 5):
            dossier["municipality"] = dossier_data_split[5]
        if check_params(dossier_data_split, 6):
            dossier["cadastralNumber"] = dossier_data_split[6]
        if check_params(dossier_data_split, 7):
            dossier["longitude"] = dossier_data_split[7].replace(".", ",")
        if check_params(dossier_data_split, 8):
            dossier["latitude"] = dossier_data_split[8].replace(".", ",")

        user_request_data = {key: value for key, value in post_data.items() if key in user_request_fields}
        user_request_data_split = user_request_data[user_request_fields[0]].split(" || ")
        user_request = {}
        if check_params(user_request_data_split, 0):
            user_request["reference"] = user_request_data_split[0]
        if check_params(user_request_data_split, 1):
            user_request["type"] = user_request_data_split[1]
        if check_params(user_request_data_split, 2):
            user_request["date"] = user_request_data_split[2]
        if check_params(user_request_data_split, 3):
            user_request["description"] = user_request_data_split[3]
        if check_params(user_request_data_split, 4):
            user_request["remarks"] = user_request_data_split[4]
        if check_params(user_request_data_split, 5):
            user_request["invoiceAddres"] = user_request_data_split[5]

        contacts = []
        contacts_data = {key: value for key, value in post_data.items() if key in contacts_fields}
        for key, value in contacts_data.items():
            contact = {}
            contact_data_split = value.split(" || ")
            if check_params(contact_data_split, 0):
                contact["type"] = contact_data_split[0]
            if check_params(contact_data_split, 1):
                contact["firstName"] = contact_data_split[1]
            if check_params(contact_data_split, 2):
                contact["name"] = contact_data_split[2]
            if check_params(contact_data_split, 3):
                contact["street"] = contact_data_split[3]
            if check_params(contact_data_split, 4):
                contact["houseNumber"] = contact_data_split[4]
            if check_params(contact_data_split, 5):
                contact["poBoxNumber"] = contact_data_split[5]
            if check_params(contact_data_split, 6):
                contact["zipCode"] = contact_data_split[6]
            if check_params(contact_data_split, 7):
                contact["municipality"] = contact_data_split[7]
            if check_params(contact_data_split, 8):
                contact["countryCode"] = contact_data_split[8]
            if check_params(contact_data_split, 9):
                contact["phone"] = contact_data_split[9]
            if check_params(contact_data_split, 10):
                contact["email"] = contact_data_split[10]
            if len(contact_data_split) > 11 and check_params(contact_data_split, 11):
                contact["companyNumber"] = contact_data_split[11]
            if len(contact_data_split) > 12 and check_params(contact_data_split, 12):
                contact["nationalRegistryNumber"] = contact_data_split[12]
            contacts.append(contact)

        data = {}
        data.update(general)
        data["dossier"] = dossier
        data["request"] = user_request
        data["contacts"] = contacts
        self.logger.info(data)
        self.logger.info(json.dumps(data))

        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        return response.json()
