import pytest
import sys
import os
from unittest import mock
import firebase_admin
from firebase_admin import auth, firestore
from tensorflow.keras.models import load_model
from google.cloud import storage, exceptions
from io import BytesIO
import h5py
from google.cloud import exceptions as google_exceptions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from app import app
from datetime import datetime, timedelta


# ---------------- TEST CONNESSIONE GCS ----------------

def get_gcs_bucket():
    """Ottiene il bucket di Google Cloud Storage."""
    storage_client = storage.Client()
    bucket_name = 'osteoarthritis-portal-archive'
    print(f"Connessione al bucket: {bucket_name}")
    return storage_client.bucket(bucket_name)

def test_get_gcs_bucket():
    """Test per la connessione al bucket di Google Cloud Storage."""
    # Mock del client GCS e del metodo `bucket`
    with mock.patch('google.cloud.storage.Client') as mock_storage_client:
        # Creazione di un'istanza mockata del client GCS
        mock_client_instance = mock.MagicMock()
        mock_storage_client.return_value = mock_client_instance

        # Mock del metodo `bucket` per restituire un bucket mockato
        mock_bucket_instance = mock.MagicMock()
        mock_client_instance.bucket.return_value = mock_bucket_instance

        bucket = get_gcs_bucket()

        # Verifica che il client sia stato creato una sola volta
        mock_storage_client.assert_called_once()

        # Verifica che il metodo `bucket` sia stato chiamato con il nome corretto del bucket
        mock_client_instance.bucket.assert_called_once_with('osteoarthritis-portal-archive')

        # Verifica che il risultato della funzione sia il bucket mockato
        assert bucket == mock_bucket_instance


@pytest.mark.parametrize("user_id, user_exists, expected_status_code, expected_message", [
    ("valid_user_id", True, 200, None), # Caso di successo
    ("invalid_user_id", False, 404, "User not found") # Utente non trovato
])

def test_get_user(client, user_id, user_exists, expected_status_code, expected_message):
    """Test parametrizzato per ottenere i dati dell'utente."""

    # Dati di test per un utente
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "name": "Test",
        "family_name": "User",
        "phone_number": "1234567890",
        "role": "doctor"
    }

    # Mock del metodo db.collection().document().get() per simulare l'esistenza o meno dell'utente
    with mock.patch('app.db.collection') as mock_collection:
        mock_user_ref = mock.Mock()
        if user_exists:
            mock_user_ref.get.return_value.exists = True
            mock_user_ref.get.return_value.to_dict.return_value = user_data
        else:
            mock_user_ref.get.return_value.exists = False
        mock_collection.return_value.document.return_value = mock_user_ref

        # Chiamata all'endpoint per ottenere i dati dell'utente
        response = client.get(f'/api/get_user/{user_id}')

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        # Verifica il messaggio in base al risultato
        if expected_status_code == 200:
            assert response.json == user_data  # La risposta deve contenere i dati dell'utente
        elif expected_status_code == 404:
            assert expected_message in response.json["error"]

@pytest.mark.parametrize(
    "user_id, updates, mock_update_side_effect, expected_status_code, expected_message, expected_error",
    [
        ( # Caso di successo
            "valid_user_id", 
            {"username": "updateduser", "nome": "Updated", "cognome": "User"}, 
            None, 200, 
            "Dati aggiornati con successo!", 
            None
        ),
        ( # Utente non trovato
            "valid_user_id", 
            {"username": "updateduser", "nome": "Updated", "cognome": "User"}, 
            exceptions.GoogleCloudError("Errore Firestore"),
            400, 
            "Errore durante l'aggiornamento dei dati.", 
            "Errore Firestore"
        )
    ]
)

def test_update_user(client, user_id, updates, mock_update_side_effect, expected_status_code, expected_message, expected_error):
    """Test parametrizzato per l'aggiornamento dei dati dell'utente."""

    # Mock del metodo db.collection().document().update()
    with mock.patch('app.db.collection') as mock_collection:
        mock_user_ref = mock.Mock()
        mock_collection.return_value.document.return_value = mock_user_ref
        mock_user_ref.update.side_effect = mock_update_side_effect  # Simula errore o successo

        # Dati di test per la richiesta PATCH
        data = {
            "userId": user_id,
            **updates
        }

        # Chiamata all'endpoint per aggiornare i dati dell'utente
        response = client.patch('/update_user', json=data)

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        # Verifica il messaggio di successo o errore
        if expected_status_code == 200:
            assert expected_message in response.json["message"]
        elif expected_status_code == 400:
            assert expected_message in response.json["message"]
            assert expected_error in response.json["error"] if expected_error else True

@pytest.mark.parametrize(
    "email, mock_user_data, expected_status_code, expected_message, expected_attempts_left, expected_error",
    [
        (
            "user@example.com", # Caso di successo (3 tentativi)
            {"email": "user@example.com", "loginAttemptsLeft": 3},
            200, 
            "Attempts decremented", 
            2,
            None
        ),
        (
            "user@example.com", # Caso di successo (0 tentativi)
            {"email": "user@example.com", "loginAttemptsLeft": 0}, 
            200, 
            "Attempts decremented", 
            0,
            None
        ),
        (
            "nonexistent@example.com", # Utente non trovato
            None,
            404, 
            "User not found", 
            None, 
            "User not found"
        ),
        (
            "",  # Email mancante
            None, 
            400, 
            "Email is required", 
            None, 
            "Email is required"
        )
    ]
)
def test_decrement_login_attempts(client, email, mock_user_data, expected_status_code, expected_message, expected_attempts_left, expected_error):
    """Test parametrizzato per il decremento dei tentativi di login."""

    # Mock del metodo db.collection().where().stream() per simulare la query dell'utente
    with mock.patch('app.db.collection') as mock_collection:
        mock_user_ref = mock.Mock()
        if mock_user_data is not None:
            mock_user_ref.to_dict.return_value = mock_user_data
            mock_collection.return_value.where.return_value.stream.return_value = [mock_user_ref]
        else:
            mock_collection.return_value.where.return_value.stream.return_value = []

        # Dati di test per la richiesta POST
        data = {
            "email": email
        }

        # Chiamata all'endpoint per decrementare i tentativi
        response = client.post('/decrement-attempts', json=data)

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        # Verifica il messaggio e i tentativi rimasti
        if expected_status_code == 200:
            assert expected_message in response.json["message"]
            assert response.json["loginAttemptsLeft"] == expected_attempts_left
        elif expected_status_code == 400 or expected_status_code == 404:
            assert expected_error in response.json["error"]

@pytest.mark.parametrize(
    "email, mock_user_data, expected_status_code, expected_message, expected_attempts_left, expected_error",
    [
        (
            "user@example.com", # Caso di successo (3 tentativi)
            {"email": "user@example.com", "loginAttemptsLeft": 3},
            200, 
            "loginAttemptsLeft", 
            3,  # Tentativi rimanenti
            None
        ),
        (
            "user@example.com", # Caso di successo (0 tentativi)
            {"email": "user@example.com", "loginAttemptsLeft": 0},
            200, 
            "loginAttemptsLeft", 
            0,  # Tentativi esauriti
            None
        ),
        (
            "nonexistent@example.com", # Utente non trovato
            None, 
            404, 
            "User not found", 
            None, 
            "User not found"
        ),
        (
            "",  # Email mancante
            None, 
            400, 
            "Email is required", 
            None, 
            "Email is required"
        )
    ]
)

def test_get_attempts_left(client, email, mock_user_data, expected_status_code, expected_message, expected_attempts_left, expected_error):
    """Test parametrizzato per il recupero dei tentativi di login rimanenti."""

    # Mock del metodo db.collection().where().stream() per simulare la query dell'utente
    with mock.patch('app.db.collection') as mock_collection:
        mock_user_ref = mock.Mock()
        if mock_user_data is not None:
            mock_user_ref.to_dict.return_value = mock_user_data
            mock_collection.return_value.where.return_value.stream.return_value = [mock_user_ref]
        else:
            mock_collection.return_value.where.return_value.stream.return_value = []

        # Dati di test per la richiesta POST
        data = {
            "email": email
        }

        # Chiamata all'endpoint per ottenere i tentativi rimanenti
        response = client.post('/get-attempts-left', json=data)

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        # Verifica il messaggio e i tentativi rimasti
        if expected_status_code == 200:
            assert expected_message in response.json
            assert response.json["loginAttemptsLeft"] == expected_attempts_left
        elif expected_status_code == 400 or expected_status_code == 404:
            assert expected_error in response.json["error"]

@pytest.mark.parametrize(
    "doctors_in_db, expected_status_code, expected_message",
    [
        (
            [{"email": "doctor1@example.com", "name": "Dr. John Doe", "role": "doctor"}],  # Caso di successo
            200, 
            None 
        ),
        (
            [],  # Caso in cui non ci sono dottori
            404, 
            "Nessun dottore trovato"
        )
    ]
)

def test_get_doctors(client, doctors_in_db, expected_status_code, expected_message):
    """Test parametrizzato per il recupero dei dottori"""
    
    # Mock del metodo db.collection().where().stream() per simulare i dati dei dottori nel database
    with mock.patch('app.db.collection') as mock_collection:
        mock_doctor_ref = mock.Mock()
        
        # Se ci sono dottori, simuliamo il ritorno dei dati
        if doctors_in_db:
            mock_doctor_ref.to_dict.return_value = doctors_in_db[0]
            mock_collection.return_value.where.return_value.stream.return_value = [mock_doctor_ref]
        else:
            # Se non ci sono dottori, simuliamo una risposta vuota
            mock_collection.return_value.where.return_value.stream.return_value = []

        # Chiamata all'endpoint per ottenere la lista dei dottori
        response = client.get('/api/doctors')

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        if expected_status_code == 200:
            # Se ci sono dottori, verifica che la risposta contenga i dati dei dottori
            assert isinstance(response.json, list)
            assert len(response.json) > 0
        elif expected_status_code == 404:
            # Se non ci sono dottori, verifica il messaggio di errore
            assert expected_message in response.json["message"]

@pytest.mark.parametrize(
    "patients_in_db, expected_status_code, expected_message",
    [
        (
            [{"email": "patient1@example.com", "name": "John Doe", "role": "patient"}],  # Caso di successo
            200, 
            None 
        ),
        (
            [],  # Caso in cui non ci sono pazienti
            404, 
            "Nessun paziente trovato"
        )
    ]
)

def test_get_patients(client, patients_in_db, expected_status_code, expected_message):
    """Test parametrizzato per il recupero dei pazienti."""
    
    # Mock del metodo db.collection().where().stream() per simulare i dati dei pazienti nel database
    with mock.patch('app.db.collection') as mock_collection:
        mock_patient_ref = mock.Mock()
        
        # Se ci sono pazienti, simuliamo il ritorno dei dati
        if patients_in_db:
            mock_patient_ref.to_dict.return_value = patients_in_db[0]
            mock_collection.return_value.where.return_value.stream.return_value = [mock_patient_ref]
        else:
            # Se non ci sono pazienti, simuliamo una risposta vuota
            mock_collection.return_value.where.return_value.stream.return_value = []

        # Chiamata all'endpoint per ottenere la lista dei pazienti
        response = client.get('/api/patients')

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        if expected_status_code == 200:
            # Se ci sono pazienti, verifica che la risposta contenga i dati dei pazienti
            assert isinstance(response.json, list)
            assert len(response.json) > 0
        elif expected_status_code == 404:
            # Se non ci sono pazienti, verifica il messaggio di errore
            assert expected_message in response.json["message"]

@pytest.mark.parametrize(
    "patients_in_db, expected_status_code, expected_message",
    [
        (
            [{"userId": "12345", "name": "Patient One", "DoctorRef": "doctor_123"}],  # Caso di successo
            200, 
            None 
        ),
        (
            [],  # Caso in cui non ci pazienti per il dottore selezionato
            404, 
            "Nessun paziente trovato per il dottore selezionato"
        )
    ]
)

def test_get_patients_from_doctor(client, patients_in_db, expected_status_code, expected_message):
    """Test parametrizzato per il recupero dei pazienti associati ad un dottore."""
    doctor_id = "doctor_123"
    
    # Mock del metodo db.collection().where().stream() per simulare i dati dei pazienti nel database
    with mock.patch('app.db.collection') as mock_collection, \
         mock.patch('app.auth.get_user') as mock_auth_get_user:

        mock_patient_ref = mock.Mock()

        # Se ci sono pazienti, simuliamo il ritorno dei dati
        if patients_in_db:
            mock_patient_ref.to_dict.return_value = patients_in_db[0]
            mock_collection.return_value.where.return_value.stream.return_value = [mock_patient_ref]
            mock_auth_get_user.return_value.email_verified = True
        else:
            # Se non ci sono pazienti, simuliamo una risposta vuota
            mock_collection.return_value.where.return_value.stream.return_value = []
        
        # Chiamata all'endpoint per ottenere i pazienti
        response = client.get(f'/api/{doctor_id}/patients')

        # Verifica il codice di stato
        assert response.status_code == expected_status_code
        
        if expected_status_code == 200:
            # Se ci sono pazienti, verifica che la risposta contenga i dati dei pazienti
            assert isinstance(response.json, list)
            assert len(response.json) > 0
        elif expected_status_code == 404:
            # Se non ci sono pazienti, verifica il messaggio di errore
            assert expected_message in response.json["message"]

@pytest.mark.parametrize(
    "doctor_id, patient_id, operation_date, description, expected_status, expected_message",
    [
        # Caso di successo
        ("doctor123", "patient456", (datetime.now() + timedelta(days=5)).isoformat(), "Test operation", 201, "Operazione pianificata"),
        
        # Dati mancanti
        (None, "patient456", (datetime.now() + timedelta(days=5)).isoformat(), "Test operation", 400, "Dati mancanti (doctorId, patientId, operationDate)"),
        ("doctor123", None, (datetime.now() + timedelta(days=5)).isoformat(), "Test operation", 400, "Dati mancanti (doctorId, patientId, operationDate)"),
        ("doctor123", "patient456", None, "Test operation", 400, "Dati mancanti (doctorId, patientId, operationDate)"),
        
        # Formato della data non valido
        ("doctor123", "patient456", "invalid-date", "Test operation", 400, "Formato data non valido (usa ISO 8601: YYYY-MM-DD)"),
        
        # Data passata
        ("doctor123", "patient456", (datetime.now() - timedelta(days=1)).isoformat(), "Test operation", 400, "La data deve essere futura"),
    ]
)
def test_add_operation_parametrized(client, doctor_id, patient_id, operation_date, description, expected_status, expected_message):
    """Test parametrizzato per l'aggiunta di un'operazione."""
    # Mock della collezione Firestore
    with mock.patch('app.db.collection') as mock_collection:
        # Mock per il riferimento alla collezione 'operations'
        mock_operations_ref = mock.MagicMock()
        mock_collection.return_value = mock_operations_ref

        # Mock per il metodo `add` della collezione solo per il caso valido
        if expected_status == 201:
            mock_add_result = (None, mock.Mock(id="mock_operation_id"))
            mock_operations_ref.add.return_value = mock_add_result

        # Prepara i dati della richiesta
        data = {
            "doctorId": doctor_id,
            "patientId": patient_id,
            "operationDate": operation_date,
            "description": description,
        }

        # Effettua la chiamata all'endpoint
        response = client.post('/api/operations', json=data)

        # Verifica del codice di stato
        assert response.status_code == expected_status

        # Verifica del messaggio di risposta
        response_data = response.json
        if expected_status == 201:
            assert response_data["message"] == expected_message
            assert response_data["id"] == "mock_operation_id"
            assert response_data["operation"]["doctorId"] == doctor_id
            assert response_data["operation"]["patientId"] == patient_id
            assert response_data["operation"]["operationDate"] == operation_date
            assert response_data["operation"]["description"] == description
        else:
            assert response_data["error"] == expected_message

@pytest.mark.parametrize("patient_id, mock_operations_data, mock_exception, expected_status", [
    # Caso di successo: due operazioni trovate
    (
        "patient123",
        [
            {
                "id": "op1",
                "doctorId": "doctor123",
                "patientId": "patient123",
                "operationDate": "2025-01-10T10:00:00",
                "description": "Test operation 1",
                "notificationStatus": "pending",
                "createdAt": "2025-01-01T10:00:00",
            },
            {
                "id": "op2",
                "doctorId": "doctor456",
                "patientId": "patient123",
                "operationDate": "2025-02-15T15:00:00",
                "description": "Test operation 2",
                "notificationStatus": "completed",
                "createdAt": "2025-01-05T15:00:00",
            },
        ],
        None,
        200,
    ),
    # Eccezione durante la query
    (
        "patient123",
        [],
        Exception("Errore nel database"),
        500,
    ),
    # Nessuna operazione trovata
    (
        "patient456",
        [],
        None,
        200,
    ),
])

def test_get_patient_operations(client, patient_id, mock_operations_data, mock_exception, expected_status):
    """Test parametrizzato per recuperare le operazioni di un paziente."""
    with mock.patch('app.db.collection') as mock_collection:
        # Simula il comportamento della query
        mock_operations_ref = mock.MagicMock()
        mock_collection.return_value = mock_operations_ref

        if mock_exception:
            # Simula un'eccezione
            mock_operations_ref.where.side_effect = mock_exception
        else:
            # Crea i mock delle operazioni basandosi sui dati forniti
            mock_operations = [
                mock.Mock(
                    id=op["id"],
                    to_dict=lambda op_data=op: op_data  # Restituisce i dati come dict
                ) for op in mock_operations_data
            ]
            # Simula i risultati della query
            mock_operations_query = mock.MagicMock()
            mock_operations_query.stream.return_value = mock_operations
            mock_operations_ref.where.return_value = mock_operations_query

        # Chiamata all'endpoint
        response = client.get(f'/api/patients/{patient_id}/operations')

        # Verifica del codice di stato
        assert response.status_code == expected_status

        # Verifica del contenuto della risposta
        if not mock_exception:
            assert response.json == mock_operations_data
        else:
            assert response.json == {"error": str(mock_exception)}

        # Verifica che la query sia stata eseguita correttamente solo se non ci sono errori
        if not mock_exception:
            mock_operations_ref.where.assert_called_once_with('patientId', '==', patient_id)

@pytest.mark.parametrize(
    "file_url, filename, mock_response, expected_status_code, expected_error_message, expected_file_content",
    [
        # Caso di successo: URL valido e risposta 200
        (
            "http://example.com/radiograph.png",  
            "test_image.png",  
            mock.Mock(status_code=200, content=b'fake-image-content'),  
            200,  
            None,  
            b'fake-image-content'  
        ),
        #  URL mancante
        (
            None,  
            "test_image.png",
            None,  
            400,  
            "File URL is missing",  
            None  
        ),
        # Errore durante il download
        (
            "http://example.com/radiograph.png",  
            "test_image.png",  
            mock.Mock(status_code=500, content=b''),  
            500,  
            "Failed to fetch radiograph",  
            None  
        )
    ]
)

def test_download_radiograph(client, file_url, filename, mock_response, expected_status_code, expected_error_message, expected_file_content):
    """Test parametrizzato per il download di una radiografia"""
    with mock.patch('requests.get', return_value=mock_response):
        
        # Chiamata all'endpoint
        query_string = {'url': file_url, 'filename': filename}
        response = client.get('/api/download-radiograph', query_string=query_string)
        
        # Verifica del codice di stato
        assert response.status_code == expected_status_code
        
        # Verifica del messaggio di errore
        if expected_error_message:
            assert response.json['error'] == expected_error_message
        
        # Verifica del contenuto del file
        if expected_file_content:
            assert response.data == expected_file_content
