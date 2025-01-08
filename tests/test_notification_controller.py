import pytest
from unittest.mock import patch

@pytest.mark.parametrize(
    "payload, mock_side_effect, expected_status_code, expected_key, expected_substring",
    [
        # Caso 1: Invio riuscito con campi completi
        (
            {
                "patientId": "paziente123",
                "message": "Messaggio di test",
                "date": "2025-01-08",
                "time": "14:30",
                "sentAt": "2025-01-08T14:00:00"
            },
            None, 
            200,
            "message",
            "Notifica inviata con successo",
        ),
        # Caso 2: Manca un campo obbligatorio 
        (
            {
                "message": "Manca patientId",
                "date": "2025-01-08",
                "time": "14:30",
                "sentAt": "2025-01-08T14:00:00"
            },
            KeyError("patientId"), 
            500,
            "error",
            "patientId",
        ),
        # Caso 3: Eccezione generica dal metodo create_notification() di Firestore 
        (
            {
                "patientId": "pazienteXYZ",
                "message": "Altra notifica",
                "date": "2025-01-08",
                "time": "15:00",
                "sentAt": "2025-01-08T14:00:00"
            },
            Exception("Errore generico"),
            500,
            "error",
            "Errore generico"
        ),
    ],
)
@patch("utils.firestore_utils.FirestoreManager.create_notification")
def test_send_notification(
    mock_create_notification,
    payload,
    mock_side_effect,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa il comportamento dell'endpoints /send-notification in tre casi:
    1) Invio riuscito
    2) Campo obbligatorio mancante 
    3) Eccezione generica dal metodo create_notification() di Firestore 
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_create_notification.side_effect = mock_side_effect
    else:
        mock_create_notification.return_value = ("notif123", {"dummy": "data"})

    # Richiesta POST all'endpoint /api/notifications
    response = client.post("/api/notifications", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_substring in str(json_data[expected_key])


@pytest.mark.parametrize(
    "patient_id, mock_side_effect, mock_return_value, expected_status_code, expected_key, expected_value_substr",
    [
        # Caso 1: patientId mancante 
        (
            None,
            None,
            None,
            400,
            "error",
            "patientId è richiesto"
        ),
        # Caso 2: Paziente trovato, restituisce lista di notifiche 
        (
            "paziente123",
            None,
            [{"id": "notif1", "message": "Test notification"}],
            200,
            "notifications",
            "notif1",
        ),
        # Caso 3: Eccezione generica 
        (
            "pazienteEccezione",
            Exception("Errore Firestore"),
            None,
            500,
            "error",
            "Errore Firestore",
        ),
    ]
)
@patch("utils.firestore_utils.FirestoreManager.get_user_notifications")
def test_get_notifications(
    mock_get_user_notifications,
    patient_id,
    mock_side_effect,
    mock_return_value,
    expected_status_code,
    expected_key,
    expected_value_substr,
    client
):
    """
    Testa il comportamento dell'endpoint /get-notifications in tre scenari:
    1) patientId mancante
    2) Lista di notifiche recuperata con successo
    3) Eccezione generica
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_get_user_notifications.side_effect = mock_side_effect
    else:
        mock_get_user_notifications.return_value = mock_return_value or []

    # Costruzione dell'URL con query param, se patient_id è presente
    if patient_id is not None:
        url = f"/api/notifications?patientId={patient_id}"
    else:
        url = "/api/notifications" 

    response = client.get(url)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value_substr in str(json_data[expected_key])

@pytest.mark.parametrize(
    "notification_id, mock_side_effect, mock_return_value, expected_status_code, expected_key, expected_value_substr",
    [
        # Caso 1: Notifica marcata come letta
        (
            "notif123",
            None,
            True, 
            200,
            "message",
            "Notifica segnata come letta",
        ),
        # Caso 2: Notifica non trovata
        (
            "missingNotif",
            None,
            False, 
            404,
            "error",
            "Notifica non trovata",
        ),
        # Caso 3: Eccezione generica 
        (
            "badNotifId",
            Exception("Errore generico"),
            None,
            500,
            "error",
            "Errore generico",
        ),
    ]
)
@patch("utils.firestore_utils.FirestoreManager.mark_notification_read")
def test_mark_notification_as_read(
    mock_mark_notification_read,
    notification_id,
    mock_side_effect,
    mock_return_value,
    expected_status_code,
    expected_key,
    expected_value_substr,
    client
):
    """
    Testa il comportamento dell'endpoint /mark_notification_as_read in tre scenari:
    1) Notifica trovata e segnata come letta
    2) Notifica non trovata
    3) Eccezione generica
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_mark_notification_read.side_effect = mock_side_effect
    else:
        mock_mark_notification_read.return_value = mock_return_value

    # Costruzione URL e richiesta PATCH
    url = f"/api/notifications/{notification_id}"
    response = client.patch(url)

    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_value_substr in str(json_data[expected_key])