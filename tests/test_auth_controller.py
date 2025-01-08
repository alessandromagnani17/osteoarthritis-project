import pytest
from unittest import mock
from utils.email_utils import EmailManager
from unittest.mock import MagicMock, patch
from controllers.auth_controller import AuthController
from firebase_admin import auth

@pytest.mark.parametrize(
    "payload, mock_create_user, mock_send_email, expected_status, expected_message",
    [
        # Caso positivo
        (
            {
                'email': 'test@example.com',
                'password': 'SecurePass123!',
                'username': 'test_user',
                'nome': 'Test',
                'cognome': 'User',
                'data': '1990-01-01',
                'telefono': '1234567890',
                'gender': 'M',
                'address': '123 Test St.',
                'cap_code': '12345',
                'tax_code': 'ABCDEF12G34H567I',
                'role': 'doctor',
                'doctorID': 'DOC12345'
            },
            ('test_uid', {'username': 'test_user', 'email': 'test@example.com'}),
            True,
            200,
            "User registered successfully. Please check your email for the confirmation link."
        ),
        # Caso negativo: errore in FirestoreManager durante la creazione dell'utente 
        (
            {
                'email': 'test@example.com',
                'password': 'SecurePass123!',
                'username': 'test_user'
            },
            Exception("Errore durante la creazione dell'utente"),
            None,
            400,
            "Controlla i dati forniti."
        )
    ]
)

@patch('utils.firestore_utils.FirestoreManager')
@patch('utils.email_utils.EmailManager')
def test_register_user(mock_email_manager, mock_firestore_manager, client, payload, mock_create_user, mock_send_email, expected_status, expected_message):
    """
    Testa il comportamento dell'endpoint /register in due scenari:
    1) Caso di successo
    2) Caso di errore in FirestoreManager.create_user
    """
    # Configura il mock di FirestoreManager.create_user
    if isinstance(mock_create_user, Exception):
        mock_firestore_manager.return_value.create_user.side_effect = mock_create_user
    else:
        mock_firestore_manager.return_value.create_user.return_value = mock_create_user

    # Configura il mock di EmailManager.send_email
    mock_email_manager.return_value.send_email.return_value = mock_send_email

    # Simula una richiesta POST alla rotta /register
    response = client.post('/register', json=payload)

    # Asserzioni
    assert response.status_code == expected_status
    json_data = response.get_json()
    assert expected_message in json_data['message']
    if response.status_code == 200:
        assert 'response' in json_data
        assert json_data['response']['email'] == payload['email']

@pytest.mark.parametrize(
    "mock_scenario, payload, expected_status_code, expected_key, expected_value",
    [
        # Caso 1: Token valido
        (
            "valid_token",
            {"idToken": "valid-id-token"},
            200,
            "message",
            "Login successful",
        ),
        # Caso 2: Token mancante
        (
            "missing_token",
            {},
            400,
            "error",
            "ID token is required",
        ),
        # Caso 3: Token non valido
        (
            "invalid_token",
            {"idToken": "invalid-id-token"},
            401,
            "error",
            "Invalid ID token",
        ),
    ]
)

@patch("firebase_admin.auth.verify_id_token")
@patch("firebase_admin.auth.get_user")
@patch("utils.firestore_utils.FirestoreManager.get_document")
def test_login_parametrized(
    mock_get_document,
    mock_get_user,
    mock_verify_id_token,
    mock_scenario,
    payload,
    expected_status_code,
    expected_key,
    expected_value,
    client
):
    """
    Testa il comportamento dell'endpoint /login in tre scenari:
    1) Token valido
    2) Token mancante
    3) Token non valido
    """
    if mock_scenario == "valid_token":
        # Configurazione Mock per token valido
        mock_verify_id_token.return_value = {"uid": "test-uid"}
        mock_get_user.return_value = type(
            "MockedUser", (object,), {"uid": "test-uid", "email": "test@example.com"}
        )
        mock_get_document.return_value = {
            "username": "testuser",
            "email": "test@example.com",
            "loginAttemptsLeft": 3
        }

    elif mock_scenario == "invalid_token":
        # Configurazione Mock per token non valido
        mock_verify_id_token.side_effect = auth.InvalidIdTokenError("Invalid token")

    # Invio richiesta POST all'endpoint /login
    response = client.post("/login", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value in json_data[expected_key]

@pytest.mark.parametrize(
    "scenario, payload, mock_user, mock_side_effect, expected_status_code, expected_key, expected_value",
    [
        # Caso 1: Email mancante
        (
            "missing_email",
            {},
            None,
            None,
            400,
            "error",
            "Email is required",
        ),
        # Caso 2: Utente trovato e email verificata
        (
            "verified_email",
            {"email": "verified@example.com"},
            type("MockedUser", (object,), {"email_verified": True}),
            None,
            200,
            "message",
            "Email verified",
        ),
        # Caso 3: Utente trovato e email non verificata
        (
            "unverified_email",
            {"email": "unverified@example.com"},
            type("MockedUser", (object,), {"email_verified": False}),
            None,
            403,
            "error",
            "non è stata verificata",
        ),
        # Caso 4: Utente non trovato
        (
            "user_not_found",
            {"email": "notfound@example.com"},
            None,
            auth.UserNotFoundError("User not found"),
            404,
            "error",
            "User not found",
        ),
        # Caso 5: Errore interno generico
        (
            "generic_error",
            {"email": "error@example.com"},
            None,
            Exception("Internal server error"),
            500,
            "error",
            "Internal server error",
        ),
    ]
)

@patch("firebase_admin.auth.get_user_by_email")
def test_check_email_verification(
    mock_get_user_by_email,
    scenario,
    payload,
    mock_user,
    mock_side_effect,
    expected_status_code,
    expected_key,
    expected_value,
    client
):
    """
    Testa il comportamento dell'endpoint /check_email_verification in cinque casi:
    1) Email mancante
    2) Email verificata
    3) Email non verificata
    4) Utente non trovato
    5) Errore interno
    """
    if mock_side_effect:
        mock_get_user_by_email.side_effect = mock_side_effect
    else:
        mock_get_user_by_email.return_value = mock_user

    # Invio della richiesta POST all'endpoint /check-email-verification
    response = client.post("/check-email-verification", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value in str(json_data[expected_key])

@pytest.mark.parametrize(
    "route_uid, mock_user, mock_side_effect, expected_status_code, expected_key, expected_value",
    [        
        # Caso 1: Utente non trovato 
        (
            "notfounduid",
            None,
            auth.UserNotFoundError("Utente non trovato"),
            404,
            "error",
            "Utente non trovato",
        ),
        
        # Caso 2: Utente già verificato 
        (
            "verifieduid",
            type("MockedUser", (object,), {"email_verified": True}),
            None,
            200,
            "message",
            "Email già verificata!",
        ),
        
        # Caso 3: Utente non verificato 
        (
            "unverifieduid",
            type("MockedUser", (object,), {"email_verified": False}),
            None,
            200,
            "message",
            "Email verificata con successo!",
        ),

        # Caso 4: Errore generico interno 
        (
            "erroruid",
            None,
            Exception("Errore generico"),
            500,
            "error",
            "Errore generico",
        ),
    ]
)

@patch("firebase_admin.auth.update_user")
@patch("firebase_admin.auth.get_user")
def test_verify_email(
    mock_get_user,
    mock_update_user,
    route_uid,
    mock_user,
    mock_side_effect,
    expected_status_code,
    expected_key,
    expected_value,
    client
):
    """
    Testa il comportamento dell'endpoint /verify-email in quattro scenari:
    1) Utente non trovato
    2) Utente già verificato
    3) Utente non verificato
    4) Errore generico interno
    """
    # Configurazione del Mock: get_user
    if mock_side_effect:
        mock_get_user.side_effect = mock_side_effect
    else:
        mock_get_user.return_value = mock_user

    mock_update_user.return_value = None

    # Costruzione dell'endpoint
    if route_uid is not None:
        endpoint = f"/verify-email/{route_uid}"
    else:
        endpoint = "/verify-email"

    response = client.get(endpoint)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value in str(json_data[expected_key])

@pytest.mark.parametrize(
    "payload, mock_update_attempts_return, side_effect, expected_status_code, expected_key, expected_value",
    [
        # Caso 1: UID mancante
        (
            {"password": "new-secret-password"},  
            None, 
            None,
            400,
            "error",
            "UID e password sono obbligatori.",
        ),
        # Caso 2: Password mancante
        (
            {"uid": "test-uid"}, 
            None,
            None,
            400,
            "error",
            "UID e password sono obbligatori.",
        ),
        # Caso 3: Errore Firestore (update_login_attempts restituisce False)
        (
            {"uid": "test-uid", "password": "new-secret-password"},
            False, 
            None,
            500,
            "error",
            "Errore durante l'aggiornamento dei tentativi di login",
        ),
        # Caso 4: Successo
        (
            {"uid": "test-uid", "password": "new-secret-password"},
            True,
            None,
            200,
            "message",
            "Password aggiornata con successo.",
        ),
        # Caso 5: Eccezione generale
        (
            {"uid": "test-uid", "password": "new-secret-password"},
            None,
            Exception("Errore generico"),
            500,
            "error",
            "Errore: Errore generico",
        ),
    ]
)

@patch("firebase_admin.auth.update_user")
@patch("utils.firestore_utils.FirestoreManager.update_login_attempts")
def test_reset_password(
    mock_update_login_attempts,
    mock_update_user,
    payload,
    mock_update_attempts_return,
    side_effect,
    expected_status_code,
    expected_key,
    expected_value,
    client
):
    """
    Testa il comportamento dell'endpoint /reset-password in cinque situazioni:
    1) UID mancante
    2) Password mancante
    3) Errore nella gestione dei tentativi di login
    4) Aggiornamento completato con successo
    5) Eccezione generale
    """
    # Configurazione dei mock
    if side_effect:
        mock_update_user.side_effect = side_effect
    else:
        if mock_update_attempts_return is not None:
            mock_update_login_attempts.return_value = mock_update_attempts_return

    # Chiamata alla rotta /reset-password
    response = client.post("/reset-password", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value in str(json_data[expected_key])

@pytest.mark.parametrize(
    "payload, mock_user, mock_side_effect_auth, mock_side_effect_email, expected_status_code, expected_key, expected_msg_substring",
    [
        # Caso 1: Email mancante 
        (
            {}, 
            None,
            None,
            None,
            400,
            "error",
            "L'email è obbligatoria",
        ),
        # Caso 2: Utente esistente, email inviata con successo 
        (
            {"email": "user@example.com"},
            type("MockedUser", (object,), {"uid": "user-uid"}),
            None,
            None,
            200,
            "message",
            "Email di reset inviata con successo",
        ),
        # Caso 3: Errore nella ricerca dell’utente 
        (
            {"email": "notfound@example.com"},
            None,
            auth.UserNotFoundError("Utente non trovato"),
            None,
            500,
            "error",
            "Errore durante l'invio del link di reset",
        ),
        # Caso 4: Errore generico nell'invio dell’email
        (
            {"email": "user2@example.com"},
            type("MockedUser", (object,), {"uid": "user2-uid"}),
            None,
            Exception("SMTP error"),
            500,
            "error",
            "Errore durante l'invio del link di reset: SMTP error",
        ),
    ],
)

@patch("utils.email_utils.EmailManager.send_email")
@patch("firebase_admin.auth.get_user_by_email")
def test_send_reset_email(
    mock_get_user_by_email,
    mock_send_email,
    payload,
    mock_user,
    mock_side_effect_auth,
    mock_side_effect_email,
    expected_status_code,
    expected_key,
    expected_msg_substring,
    client
):
    """
    Testa il comportamento dell'endpoint /send-reset-email in quatro scenari:
    1) Email mancante
    2) Utente esistente, invio email ok
    3) Errore nella ricerca dell'utente
    4) Errore nell'invio dell'email
    """
    # Configurazione del mock di get_user_by_email
    if mock_side_effect_auth:
        mock_get_user_by_email.side_effect = mock_side_effect_auth
    else:
        mock_get_user_by_email.return_value = mock_user

    # Configurazione del mock di send_email
    if mock_side_effect_email:
        mock_send_email.side_effect = mock_side_effect_email
    else:
        mock_send_email.return_value = True 

    # Invio richiesta POST all'endpoint /send-reset-email
    response = client.post("/send-reset-email", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_msg_substring in str(json_data[expected_key])

@pytest.mark.parametrize(
    "payload, query_result, update_result, expected_status_code, expected_key, expected_value_substr",
    [
        # Caso 1: Email mancante
        (
            {}, 
            None,
            None,
            400,
            "error",
            "Email is required",
        ),
        # Caso 2: Utente non trovato → query_documents restituisce lista vuota 
        (
            {"email": "notfound@example.com"},
            [],      # nessun documento trovato
            None,
            404,
            "error",
            "User not found",
        ),
        # Caso 3: Aggiornamento riuscito
        (
            {"email": "test@example.com"},
            [{"id": "user123", "loginAttemptsLeft": 3}], 
            True, 
            200,
            "message",
            "Attempts decremented",
        ),
        # Caso 4: Aggiornamento fallito
        (
            {"email": "failupdate@example.com"},
            [{"id": "user456", "loginAttemptsLeft": 2}],
            False, 
            400,
            "error",
            "Failed to update attempts",
        ),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.update_login_attempts")
@patch("utils.firestore_utils.FirestoreManager.query_documents")
def test_decrement_attempts(
    mock_query_documents,
    mock_update_login_attempts,
    payload,
    query_result,
    update_result,
    expected_status_code,
    expected_key,
    expected_value_substr,
    client
):
    """
    Testa il comportamento dell'endpoint /decrement-attempts in quattro scenari:
    1) Email mancante
    2) Utente non trovato
    3) Aggiornamento andato a buon fine
    4) Aggiornamento fallito
    """

    # Configurazione dei mock
    mock_query_documents.return_value = query_result if query_result is not None else []

    # update_login_attempts: simula il risultato dell'aggiornamento
    if update_result is not None:
        mock_update_login_attempts.return_value = update_result

    # Invio della richiesta POST all'endpoint /decrement-attempts
    response = client.post("/decrement-attempts", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value_substr in str(json_data[expected_key])
    if expected_status_code == 200:
        assert "loginAttemptsLeft" in json_data

@pytest.mark.parametrize(
    "payload, returned_docs, expected_status_code, expected_key, expected_value",
    [
        # Caso 1: Email mancante
        (
            {},
            None,
            400,
            "error",
            "Email is required",
        ),
        # Caso 2: Utente non trovato
        (
            {"email": "notfound@example.com"},
            [],
            404,
            "error",
            "User not found",
        ),
        # Caso 3: Utente trovato con loginAttemptsLeft = 3
        (
            {"email": "test@example.com"},
            [{"loginAttemptsLeft": 3}],
            200,
            "loginAttemptsLeft",
            3,
        ),
        # Caso 4: Utente trovato senza campo "loginAttemptsLeft"
        (
            {"email": "zero@example.com"},
            [{}],
            200,
            "loginAttemptsLeft",
            0,
        ),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.query_documents")
def test_get_attempts_left(
    mock_query_documents,
    payload,
    returned_docs,
    expected_status_code,
    expected_key,
    expected_value,
    client
):
    """
    Testa il comportamento dell'endpoint /get-attempts-left nei seguenti scenari:
    1) Email mancante
    2) Utente non trovato
    3) Utente trovato con un valore di loginAttemptsLeft
    4) Utente trovato ma senza campo "loginAttemptsLeft"
    """

    # Configurazione del mock di query_documents
    if returned_docs is not None:
        mock_query_documents.return_value = returned_docs
    else:
        mock_query_documents.return_value = []

    # Richiesta POST all'endpoint /get-attempts-left
    response = client.post("/get-attempts-left", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    if expected_status_code != 200:
        assert expected_value in str(json_data[expected_key])
    else:
        assert json_data[expected_key] == expected_value