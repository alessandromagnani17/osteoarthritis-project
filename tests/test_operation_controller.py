import pytest
from unittest.mock import patch

@pytest.mark.parametrize(
    "payload, mock_side_effect, mock_return_value, expected_status_code, expected_key, expected_substring",
    [
        # Caso 1: Operazione creata con successo
        (
            {
                "doctorId": "doc123",
                "patientId": "pat456",
                "operationDate": "2100-01-01T10:00:00",
                "description": "Operazione test"
            },
            None, 
            ("op789", {"dummy": "data"}), 
            201,
            "message",
            "Operazione pianificata",
        ),
        # Caso 2: ValueError (data passata) 
        (
            {
                "doctorId": "doc123",
                "patientId": "pat456",
                "operationDate": "2020-01-01T10:00:00",
            },
            ValueError("La data deve essere futura"),
            None,
            400,
            "error",
            "La data deve essere futura",
        ),
        # Caso 3: Eccezione generica 
        (
            {
                "doctorId": "docABC",
                "patientId": "patXYZ",
                "operationDate": "2123-12-31T09:00:00",
            },
            Exception("Errore generico"),
            None,
            500,
            "error",
            "Errore interno del server",
        ),
    ]
)
@patch("utils.firestore_utils.FirestoreManager.create_operation")
def test_add_operation(
    mock_create_operation,
    payload,
    mock_side_effect,
    mock_return_value,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa il comportamento dell'endpoint /add-operation in tre scenari:
    1) Creazione operazione riuscita
    2) ValueError (data passata)
    3) Eccezione generica
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_create_operation.side_effect = mock_side_effect
    else:
        mock_create_operation.return_value = mock_return_value or ("opID", {})

    # Invio POST a /api/operations
    response = client.post("/api/operations", json=payload)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_substring in str(json_data[expected_key])

@pytest.mark.parametrize(
    "patient_id, mock_side_effect, mock_return_docs, expected_status_code, expected_value_substr",
    [
        # Caso di successo: Operazioni restituite con successo
        (
            "pat123",
            None,
            [
                {"id": "op1", "description": "Operazione 1"},
                {"id": "op2", "description": "Operazione 2"}
            ],
            200,
            "op1"
        ),
        # Caso di errore: Errore generico
        (
            "patError",
            Exception("Errore Firestore"),
            None,
            500,
            "Errore Firestore"
        ),
    ]
)
@patch("utils.firestore_utils.FirestoreManager.query_documents")
def test_get_patient_operations(
    mock_query_documents,
    patient_id,
    mock_side_effect,
    mock_return_docs,
    expected_status_code,
    expected_value_substr,
    client
):
    """
    Testa il comportamento dell'endpoint /get-patient-operations in due casi:
    1) Lista di operazioni recuperata correttamente
    2) Eccezione generica
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_query_documents.side_effect = mock_side_effect
    else:
        mock_query_documents.return_value = mock_return_docs or []

    # Costruzione URL e richiesta GET
    url = f"/api/patients/{patient_id}/operations"
    response = client.get(url)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    if expected_status_code == 200:
        # Caso di successo -> JSON con lista di operazioni
        assert isinstance(json_data, list)
        assert any(expected_value_substr in str(op) for op in json_data)
    else:
        # Caso di errore -> JSON con chiave "error"
        assert "error" in json_data
        assert expected_value_substr in json_data["error"]