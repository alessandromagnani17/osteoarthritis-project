import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.parametrize(
    "user_id, mock_return_value, expected_status_code, expected_key, expected_value",
    [
        # Caso di successo: Utente trovato
        ("user123", {"name": "John"}, 200, "name", "John"),
        # Caso di errore: Utente non trovato
        ("userNotFound", None, 404, "error", "User not found"),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.get_document")
def test_get_user(
    mock_get_document,
    user_id,
    mock_return_value,
    expected_status_code,
    expected_key,
    expected_value,
    client
):
    """
    Testa il comportamento dell'endpoint /api/get_user/<user_id> in due casi:
    1) Utente trovato
    2) Utente non trovato
    """
    # Configurazione del mock
    mock_get_document.return_value = mock_return_value

    # Richiesta GET all'endpoint /api/get_user/<user_id>
    response = client.get(f"/api/get_user/{user_id}")
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    if expected_status_code == 200:
        assert json_data[expected_key] == expected_value
    else:
        assert expected_value in json_data[expected_key]

@pytest.mark.parametrize(
    "payload, mock_update_return, expected_status_code, expected_key, expected_substring",
    [
        # Caso 1: Aggiornamento riuscito
        (
            {"userId": "user123", "name": "Mario", "family_name": "Rossi"},
            True,
            200,
            "message",
            "Dati aggiornati con successo!",
        ),
        # Caso 2: Aggiornamento fallito
        (
            {"userId": "userNotFound", "name": "Fail"},
            False,
            400,
            "error",
            "Errore durante l'aggiornamento dei dati.",
        ),
        # Caso 3: Eccezione in FirestoreManager
        (
            {"userId": "userEx", "name": "Exception"},
            Exception("Test exception"),
            400,
            "error",
            "Test exception",
        ),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.update_document")
def test_update_user(
    mock_update_document,
    payload,
    mock_update_return,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa il comportamento dell'endpoint /update_user in tre scenari:
    1) Aggiornamento riuscito
    2) Aggiornamento fallito
    3) Eccezione in FirestoreManager
    """
    # Configurazione del mock
    if isinstance(mock_update_return, Exception):
        mock_update_document.side_effect = mock_update_return
    else:
        mock_update_document.return_value = mock_update_return

    # Richiesta PATCH all'endpoint /update_user
    response = client.patch("/update_user", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_substring in json_data[expected_key]

@pytest.mark.parametrize(
    "mock_doctors, expected_status_code, expected_key, expected_substring",
    [
        # Caso di successo: Dottori trovati
        ([{"name": "Dr. Strange"}], 200, None, "Dr. Strange"),
        # Caso di errore: Nessun dottore
        ([], 404, "message", "Nessun dottore trovato"),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.get_users_by_role")
def test_get_doctors(
    mock_get_users_by_role,
    mock_doctors,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa la rotta /api/doctors in due casi:
    1) Dottori trovati
    2) Nessun dottore trovato
    """
    # Configurazione del mock
    mock_get_users_by_role.return_value = mock_doctors

    # Richiesta GET all'endpoint /api/doctors
    response = client.get("/api/doctors")
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    if expected_status_code == 200:
        # Ritorno di una lista di dottori
        assert isinstance(json_data, list)
        assert expected_substring in str(json_data)
    else:
        # "message": "Nessun dottore trovato"
        assert expected_key in json_data
        assert expected_substring in json_data[expected_key]

@pytest.mark.parametrize(
    "mock_patients, expected_status_code, expected_key, expected_substring",
    [
        # Caso di successo: Pazienti trovati
        ([{"name": "PatientOne"}], 200, None, "PatientOne"),
        # Caso di errore: Nessun paziente trovato
        ([], 404, "message", "Nessun paziente trovato"),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.get_users_by_role")
def test_get_patients(
    mock_get_users_by_role,
    mock_patients,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa la rotta /api/patients in due casi:
    1) Pazienti trovati
    2) Nessun paziente trovato
    """
    # Configurazione del mock
    mock_get_users_by_role.return_value = mock_patients

    # Richiesta GET all'endpoint /api/patients
    response = client.get("/api/patients")
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    if expected_status_code == 200:
        assert isinstance(json_data, list)
        assert expected_substring in str(json_data)
    else:
        assert expected_key in json_data
        assert expected_substring in json_data[expected_key]

@pytest.mark.parametrize(
    "doctor_id, mock_patients, mock_auth_side_effects, expected_status_code, expected_key, expected_substring",
    [
        # Caso 1: Pazienti trovati e verificati
        (
            "doctorXYZ",
            [
                {"userId": "patient1"},
                {"userId": "patient2"},
            ],
            [True, True],  
            200,
            None,
            "patient1",  
        ),
        # Caso 2: Pazienti trovati ma nessuno verificato
        (
            "doctorNoVerified",
            [
                {"userId": "p1"},
                {"userId": "p2"},
            ],
            [False, False],
            404,
            "message",
            "Nessun paziente trovato per il dottore selezionato",
        ),
        # Caso 3: Eccezione generica
        (
            "doctorErr",
            [],
            None,
            500,
            "error",
            "Something wrong",
        ),
    ]
)

@patch("utils.firestore_utils.FirestoreManager.get_doctor_patients")
@patch("firebase_admin.auth.get_user")
def test_get_patients_from_doctor(
    mock_get_user,
    mock_get_doctor_patients,
    doctor_id,
    mock_patients,
    mock_auth_side_effects,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa la rotta /api/<doctor_id>/patients in tre scenari:
    1) Pazienti trovati e verificati
    2) Pazienti trovati ma nessuno verificato
    3) Eccezione generica
    """
    # Configurazione del mock
    if expected_status_code == 500:
        mock_get_doctor_patients.side_effect = Exception("Something wrong")
    else:
        mock_get_doctor_patients.return_value = mock_patients
        # Se ci sono pazienti, si settano side_effect per simulare get_user(...)
        if mock_auth_side_effects is not None:
            user_objects = []
            for verified in mock_auth_side_effects:
                user_mock = MagicMock()
                user_mock.email_verified = verified
                user_objects.append(user_mock)
            mock_get_user.side_effect = user_objects

    # Richiesta GET all'endpoint /api/<doctor_id>/patients
    response = client.get(f"/api/{doctor_id}/patients")
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    if expected_status_code == 200:
        assert isinstance(json_data, list)
        assert expected_substring in str(json_data)
    elif expected_status_code == 404:
        assert expected_key in json_data
        assert expected_substring in json_data[expected_key]
    else:
        assert expected_key in json_data
        assert expected_substring in json_data[expected_key]
