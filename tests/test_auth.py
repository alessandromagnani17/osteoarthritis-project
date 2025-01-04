import pytest
from unittest import mock
import firebase_admin
from firebase_admin import auth

def test_register(client):
    """Test per la registrazione di un nuovo utente."""
    # Mock della funzione send_email
    with mock.patch('app.send_email') as mock_send_email:
        # Dati di test per la registrazione
        data = {
            "email": "test@example.com",
            "password": "securepassword00!",
            "username": "testuser",
            "nome": "Test",
            "cognome": "User",
            "data": "2000-01-01",
            "telefono": "1234567890",
            "gender": "male",
            "address": "123 Street",
            "cap_code": "12345",
            "tax_code": "TSTUSR00A01H501Z",
            "role": "doctor",
            "doctorID": "D123"
        }
        
        # Chiamata all'endpoint di registrazione
        response = client.post('/register', json=data)
        
        # Verifica che la registrazione sia avvenuta correttamente
        assert response.status_code == 200
        assert "User registered successfully" in response.json["message"]
        
        # Verifica che la funzione send_email sia stata chiamata una volta
        mock_send_email.assert_called_once()
        
        # Verifica che l'email inviata contenga il link di verifica
        verification_link = f"http://34.122.99.160:8080/verify-email/{response.json['response']['userId']}"
        mock_send_email.assert_called_with(
            'test@example.com',
            'Verifica il tuo indirizzo email',
            f"Per favore, verifica il tuo indirizzo email cliccando il seguente link: {verification_link}"
        )

@pytest.mark.parametrize("id_token, user_exists, expected_status_code, expected_message", [
    ("valid_id_token", True, 200, "Login successful"),  # Caso di successo
    ("invalid_id_token", False, 401, "Invalid ID token"),  # Token non valido
    ("valid_id_token", False, 404, "User not found")  # Token valido ma utente non trovato
])
def test_login(client, id_token, user_exists, expected_status_code, expected_message):
    """Test parametrizzato per il login."""

    # Mock del metodo auth.verify_id_token per simulare il comportamento di un token valido/invalid
    with mock.patch('firebase_admin.auth.verify_id_token') as mock_verify_token, \
         mock.patch('firebase_admin.auth.get_user') as mock_get_user, \
         mock.patch('app.db.collection') as mock_db_collection:

        # Simula un comportamento del token
        if id_token == "valid_id_token":
            mock_verify_token.return_value = {"uid": "valid_uid"}  # UID dell'utente per un token valido
        else:
            mock_verify_token.side_effect = firebase_admin.auth.InvalidIdTokenError("Invalid ID token")

        # Simula la ricerca dell'utente in Firestore
        mock_user = mock.Mock()
        if user_exists:
            mock_user.email = "verified_user@example.com"
            mock_user.uid = "valid_uid"
            mock_get_user.return_value = mock_user

            # Simuliamo il documento dell'utente in Firestore
            mock_user_doc = mock.Mock()
            mock_user_doc.exists = True
            mock_user_doc.to_dict.return_value = {"uid": "valid_uid", "loginAttemptsLeft": 3}
            mock_db_collection.return_value.document.return_value.get.return_value = mock_user_doc
        else:
            mock_get_user.side_effect = firebase_admin.auth.UserNotFoundError("User not found")
            mock_db_collection.return_value.document.return_value.get.return_value.exists = False

        # Chiamata all'endpoint per il login
        response = client.post('/login', json={'idToken': id_token})

        # Verifica che la risposta corrisponda al codice di stato e al messaggio previsto
        assert response.status_code == expected_status_code

        # Assicurati che il corpo della risposta contenga il messaggio o errore
        response_json = response.get_json()

        # Se la risposta contiene un campo "message", verifichiamo che corrisponda al messaggio atteso
        if "message" in response_json:
            assert expected_message in response_json["message"]

        # Se la risposta contiene un campo "error", verifichiamo che corrisponda al messaggio atteso
        if "error" in response_json:
            assert expected_message in response_json["error"]

@pytest.mark.parametrize("email, email_verified, expected_status_code, expected_message", [
    ("verified_user@example.com", True, 200, "Email verified"), # Caso di successo
    ("unverified_user@example.com", False, 403, "La tua email non è stata verificata"), # Email non verificata
    ("non_existent_user@example.com", None, 404, "User not found") # Utente non trovato
])

def test_check_email_verification(client, email, email_verified, expected_status_code, expected_message):
    """Test parametrizzato per controllare se l'email è verificata."""

    # Mock del metodo auth.get_user_by_email() per simulare diversi stati di verifica
    with mock.patch('firebase_admin.auth.get_user_by_email') as mock_get_user:
        if email_verified is not None:
            mock_user = mock.Mock()
            mock_user.email_verified = email_verified
            mock_get_user.return_value = mock_user
        else:
            mock_get_user.side_effect = firebase_admin.auth.UserNotFoundError("User not found")
        
        # Chiamata all'endpoint per verificare l'email
        response = client.post('/check-email-verification', json={'email': email})

        # Verifica che la risposta corrisponda al codice di stato e al messaggio previsto
        assert response.status_code == expected_status_code
        
        # Controlla se la risposta contiene "message" o "error"
        if "message" in response.json:
            assert expected_message in response.json["message"]
        
        if "error" in response.json:
            assert expected_message in response.json["error"]

@pytest.mark.parametrize(
    "uid, user_data, expected_status_code, expected_message",
    [
        ("valid_uid", {"email_verified": True}, 200, "Email già verificata!"),  # Email già verificata
        ("valid_uid", {"email_verified": False}, 200, "Email verificata con successo!"),  # Caso di successo
        ("invalid_uid", None, 404, "Utente non trovato"),  # Utente non trovato
    ]
)
def test_verify_email(client, uid, user_data, expected_status_code, expected_message):
    """Test parametrizzato per verificare un'email."""
    
    # Mock delle funzioni di Firebase Admin SDK
    with mock.patch("app.auth.get_user") as mock_get_user, \
         mock.patch("app.auth.update_user") as mock_update_user:

        # Configura il mock per `auth.get_user`
        if user_data is not None:
            mock_user = mock.Mock()
            mock_user.email_verified = user_data["email_verified"]
            mock_get_user.return_value = mock_user
        else:
            # Passa un messaggio all'eccezione
            mock_get_user.side_effect = auth.UserNotFoundError("User not found")
        
        # Configura il mock per `auth.update_user`
        mock_update_user.return_value = None

        # Costruisci l'endpoint e fai la richiesta
        endpoint = f'/verify-email/{uid}' if uid else '/verify-email/'
        response = client.get(endpoint)

        # Verifica il codice di stato della risposta
        assert response.status_code == expected_status_code

        # Verifica il messaggio nella risposta
        if "message" in response.json:
            assert expected_message in response.json["message"]
        elif "error" in response.json:
            assert expected_message in response.json["error"]

@pytest.mark.parametrize(
    "email, user_exists, email_sent, expected_status_code, expected_message",
    [
        ("test@example.com", True, True, 200, "Email di reset inviata con successo"),  # Caso di successo
        ("test@example.com", True, False, 500, "Errore durante l'invio del link di reset"),  # Errore durante l'invio dell'email
        ("nonexistent@example.com", False, False, 500, "Errore durante l'invio del link di reset"),  # Utente non trovato
        (None, False, False, 400, "L'email è obbligatoria"),  # Email mancante
    ]
)

def test_send_reset_email(client, email, user_exists, email_sent, expected_status_code, expected_message):
    """Test parametrizzato per l'invio dell'email per il reset della password."""

    # Mock delle funzioni Firebase e dell'invio email
    with mock.patch("app.auth.get_user_by_email") as mock_get_user, \
         mock.patch("app.send_email") as mock_send_email:
        
        # Configura il mock per `auth.get_user_by_email`
        if user_exists:
            mock_user = mock.Mock()
            mock_user.uid = "valid_uid"
            mock_get_user.return_value = mock_user
        else:
            mock_get_user.side_effect = Exception("User not found")

        # Configura il mock per `send_email`
        if email_sent:
            mock_send_email.return_value = None  # Simula email inviata con successo
        else:
            mock_send_email.side_effect = Exception("Email send failed")

        # Fai la richiesta al server
        response = client.post('/send-reset-email', json={"email": email} if email else {})

        # Verifica il codice di stato
        assert response.status_code == expected_status_code

        # Verifica il messaggio nella risposta
        if "message" in response.json:
            assert expected_message in response.json["message"]
        elif "error" in response.json:
            assert expected_message in response.json["error"]

@pytest.mark.parametrize(
    "uid, new_password, update_user_side_effect, update_attempts_side_effect, expected_status_code, expected_message",
    [
        ("valid_uid", "new_password", None, None, 200, "Password aggiornata con successo."),  # Caso di successo
        (None, "new_password", None, None, 400, "UID e password sono obbligatori."),  # UID mancante
        ("valid_uid", None, None, None, 400, "UID e password sono obbligatori."),  # Password mancante
        ("valid_uid", "new_password", Exception("Errore Firebase durante l'aggiornamento"), None, 500,
         "Errore durante l'aggiornamento della password"),  # Errore durante l'aggiornamento della password
        ("valid_uid", "new_password", None, Exception("Errore Firestore durante l'aggiornamento"), 500,
         "Errore durante l'aggiornamento dei tentativi di login"),  # Errore durante l'aggiornamento dei tentativi
    ]
)

def test_reset_password(
    client, uid, new_password, update_user_side_effect, update_attempts_side_effect,
    expected_status_code, expected_message
):
    """Test parametrizzato per il reset della password"""

    # Mock per auth.update_user
    with mock.patch("app.auth.update_user") as mock_update_user, \
         mock.patch("app.db.collection") as mock_db_collection:
        
        # Configura il comportamento del mock per update_user
        if update_user_side_effect:
            mock_update_user.side_effect = update_user_side_effect
        else:
            mock_update_user.return_value = None

        # Configura il comportamento del mock per Firestore update
        mock_db = mock.Mock()
        if update_attempts_side_effect:
            mock_db.document.return_value.update.side_effect = update_attempts_side_effect
        else:
            mock_db.document.return_value.update.return_value = None
        mock_db_collection.return_value = mock_db

        # Prepara i dati per la richiesta
        data = {"uid": uid, "password": new_password}
        response = client.post("/reset-password", json=data)

        # Verifica il codice di stato della risposta
        assert response.status_code == expected_status_code

        # Verifica il messaggio nella risposta
        if "message" in response.json:
            assert expected_message in response.json["message"]
        elif "error" in response.json:
            assert expected_message in response.json["error"]