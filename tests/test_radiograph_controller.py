import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils.gcs_utils import BlobInfo
from io import BytesIO
from utils.gcs_utils import GCSManagerException
import numpy as np

@pytest.mark.parametrize(
    "patient_id, mock_side_effect, mock_return_value, expected_status_code, expected_result_check",
    [
        # Caso 1: Lista di radiografie recuperata correttamente
        (
            "pat123",
            None,
            [
                BlobInfo(
                    name="pat123/original_image_1.png",
                    url="http://gcs.url/pat123/original_image_1.png",
                    created_at=datetime(2025, 1, 1, 10, 0),
                    content_type="image/png"
                ),
                BlobInfo(
                    name="pat123/original_image_2.png",
                    url="http://gcs.url/pat123/original_image_2.png",
                    created_at=datetime(2025, 1, 2, 11, 0),
                    content_type="image/png"
                )
            ],
            200,
            "pat123/original_image_1.png"
        ),
        # Caso 2: Nessuna radiografia per quel paziente (lista vuota)
        (
            "pat999",
            None,
            [],
            200,
            "[]", 
        ),
        # Caso 3: Eccezione durante la lettura da GCS
        (
            "patError",
            Exception("Errore GCS"),
            None,
            500,
            "Errore GCS"
        ),
    ]
)

@patch("utils.gcs_utils.GCSManager.list_patient_radiographs")
def test_get_patient_radiographs(
    mock_list_patient_radiographs,
    patient_id,
    mock_side_effect,
    mock_return_value,
    expected_status_code,
    expected_result_check,
    client
):
    """
    Testa il comportamento dell'endpoint /get-patient-radiographs in tre scenari:
    1) Lista di radiografie recuperata con successo
    2) Lista vuota
    3) Eccezione generica
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_list_patient_radiographs.side_effect = mock_side_effect
    else:
        mock_list_patient_radiographs.return_value = mock_return_value or []

    # Costruzione dell'URL e richiesta GET
    url = f"/api/patients/{patient_id}/radiographs"
    response = client.get(url)
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    if expected_status_code == 200:
        assert isinstance(json_data, list)
        assert expected_result_check in str(json_data)
    else:
        assert "error" in json_data
        assert expected_result_check in json_data["error"]

@pytest.mark.parametrize(
    "url, filename, mock_status_code, mock_content, mock_side_effect, expected_status_code, expected_key, expected_substring",
    [
        # Caso 1: URL mancante 
        (
            None,
            "radiograph.png",
            None, 
            None,
            None,
            400,
            "error",
            "File URL is missing"
        ),
        # Caso 2: requests.get restituisce codice != 200
        (
            "http://example.com/radiograph1.png",
            "radio1.png",
            404,
            b"",
            None,
            500,
            "error",
            "Failed to fetch radiograph"
        ),
        # Caso 3: Eccezione durante la richiesta
        (
            "http://example.com/radiograph2.png",
            "radio2.png",
            None,
            None,
            Exception("Connessione fallita"),
            500,
            "error",
            "Connessione fallita"
        ),
        # Caso 4: Successo, restituisce file con image/png
        (
            "http://example.com/radiograph3.png",
            "radio3.png",
            200,
            b"FAKE_IMAGE_BYTES",
            None,
            200,
            None,
            None 
        ),
    ]
)

@patch("requests.get")
def test_download_radiograph(
    mock_requests_get,
    url,
    filename,
    mock_status_code,
    mock_content,
    mock_side_effect,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa il comportamento di download_radiograph nei seguenti scenari:
    1) URL mancante
    2) Codice di stato != 200
    3) Eccezione durante la richiesta
    4) Successo e restituzione del file PNG
    """

    # Configurazione del mock per requests.get
    if url is not None:
        if mock_side_effect:
            mock_requests_get.side_effect = mock_side_effect
        else:
            # Simula un oggetto Response di requests
            mock_response = MagicMock()
            mock_response.status_code = mock_status_code
            mock_response.content = mock_content
            mock_requests_get.return_value = mock_response

    # Costruzione della query string
    qs = []
    if url is not None:
        qs.append(f"url={url}")
    if filename is not None:
        qs.append(f"filename={filename}")
    query_string = "?" + "&".join(qs) if qs else ""

    response = client.get(f"/api/download-radiograph{query_string}")

    # Asserzioni
    if expected_status_code == 200:
        assert response.status_code == 200
        assert response.content_type == "image/png"
        assert "attachment" in response.headers.get("Content-Disposition", "")
        if filename is not None:
            assert filename in response.headers["Content-Disposition"]
    else:
        json_data = response.get_json()
        assert response.status_code == expected_status_code, json_data
        assert expected_key in json_data
        assert expected_substring in json_data[expected_key]

@pytest.mark.parametrize(
    "file_bytes, file_name, form_data, mock_side_effect, mock_return_value, expected_status_code, expected_key, expected_substring",
    [
        # Caso di successo: Caricamento riuscito
        (
            b"fake image data",
            "radiograph.png",
            {"patientID": "pat123", "side": "left"},
            None,
            "https://fake-public-url.com/radiograph.png",  
            200,
            "message",
            "File caricato con successo."
        ),
        # Caso di errore: Eccezione durante l'upload
        (
            b"another fake image",
            "test2.jpg",
            {"patientID": "pat456", "side": "right"},
            Exception("Errore durante upload"),
            None,
            500,
            "error",
            "Errore durante upload"
        ),
    ]
)

@patch("utils.gcs_utils.GCSManager.upload_file")
def test_upload_to_dataset(
    mock_upload_file,
    file_bytes,
    file_name,
    form_data,
    mock_side_effect,
    mock_return_value,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa il comportamento dell'endpoint /upload-to-dataset in due scenari:
    1) Caricamento riuscito
    2) Eccezione durante l'upload
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_upload_file.side_effect = mock_side_effect
    else:
        mock_upload_file.return_value = mock_return_value

    data = {
        **form_data,
        "file": (BytesIO(file_bytes), file_name)  # Simula l'upload di un file
    }

    # Invio della richiesta POST alla rotta /upload-to-dataset
    response = client.post(
        "/upload-to-dataset",
        data=data,
        content_type="multipart/form-data"
    )

    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_substring in json_data[expected_key]

@pytest.mark.parametrize(
    "user_uid, idx, mock_side_effect, mock_return_dict, expected_status_code, expected_key, expected_substring",
    [
        # Caso di successo: GCSManager.get_radiograph_info restituisce le informazioni sul paziente
        (
            "user123",
            "1",
            None, 
            {
                "Nome paziente": "John",
                "Cognome paziente": "Doe",
                "Data di nascita paziente": "01/01/1990",
                "ID radiografia": "RADIO-123"
            },
            200,
            "name",
            "John"
        ),
        # Caso di errore: GCSManagerException con chiave "error"
        (
            "userErr",
            "2",
            GCSManagerException("Errore nel recupero delle informazioni"),
            None,
            500,
            "error",
            "Errore nel recupero"
        ),
    ]
)

@patch("utils.gcs_utils.GCSManager.get_radiograph_info")
def test_get_radiographs_info(
    mock_get_radiograph_info,
    user_uid,
    idx,
    mock_side_effect,
    mock_return_dict,
    expected_status_code,
    expected_key,
    expected_substring,
    client
):
    """
    Testa la rotta /get_radiographs_info/<user_uid>/<idx> in due scenari:
    1) Successo con le informazioni restituite
    2) Errore (GCSManagerException)
    """
    # Configurazione del mock
    if mock_side_effect:
        mock_get_radiograph_info.side_effect = mock_side_effect
    else:
        mock_get_radiograph_info.return_value = mock_return_dict or {}

    # Chiamata GET alla rotta /get_radiographs_info/<user_uid>/<idx>
    response = client.get(f"/get_radiographs_info/{user_uid}/{idx}")
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    assert expected_key in json_data
    assert expected_substring in str(json_data[expected_key])

@pytest.mark.parametrize(
    "scenario, file_bytes, form_data, mock_side_effect, expected_status_code, expected_key_substring",
    [
        # Caso di successo: predizione riuscita 
        (
            "success",
            b"fake_image_data",
            {
                "userData": '{"name": "DoctorName", "family_name": "DoctorSurname", "uid": "doc-uid-001", "doctorID": "DR123"}',
                "selectedPatientID": "patient-001",
                "selectedSide": "left",
            },
            None,  # Nessuna eccezione
            200,
            "original_image",  # Nella risposta ci sarà la chiave "original_image"
        ),
        # Caso di errore: Ecccezione causata da errore interno
        (
            "error",
            b"image_for_error",
            {
                "userData": '{"name": "DoctorErr", "family_name": "DocFail", "uid": "doc-uid-XYZ", "doctorID": "DRERR"}',
                "selectedPatientID": "patient-ERR",
                "selectedSide": "right",
            },
            Exception("Simulated internal error"),
            500,
            "Simulated internal error"
        ),
    ]
)

@patch("utils.model_utils.ModelManager.generate_gradcam")
@patch("utils.model_utils.ModelManager.predict_class")
@patch("utils.model_utils.ModelManager.preprocess_image")
@patch("utils.firestore_utils.FirestoreManager.get_patient_information")
@patch("utils.gcs_utils.GCSManager.count_patient_radiographs")
@patch("utils.gcs_utils.GCSManager.save_radiograph")
def test_predict(
    mock_save_radiograph,
    mock_count_patient_radiographs,
    mock_get_patient_information,
    mock_preprocess_image,
    mock_predict_class,
    mock_generate_gradcam,
    scenario,
    file_bytes,
    form_data,
    mock_side_effect,
    expected_status_code,
    expected_key_substring,
    client
):
    """
    Testa la rotta /predict in due scenari:
    1) Predizione riuscita 
    2) Ecccezione causata da errore interno
    """

    # Configurazione del mock
    if scenario == "success":
        mock_count_patient_radiographs.return_value = 2 
        mock_get_patient_information.return_value = {
            "name": "John",
            "family_name": "Doe",
            "birthdate": "1990-01-01",
            "tax_code": "JHNDOE90A01F205X",
            "address": "Via Roma 10",
            "cap_code": "00100",
            "gender": "M",
        }
        mock_preprocess_image.return_value = (
            np.zeros((1, 224, 224, 3)),    # Immagine fake preprocessata
            np.zeros((224, 224, 3), dtype=np.uint8)  # Immagine fake RGB
        )
        mock_predict_class.return_value = (2, 0.87)  # Classe = 2, Confidenza = 0.87
        mock_generate_gradcam.return_value = np.zeros((224, 224, 3), dtype=np.uint8)
        mock_save_radiograph.return_value = {
            "original_image": "http://fake.url/original.png",
            "gradcam_image": "http://fake.url/gradcam.png",
            "info_file": "http://fake.url/info.txt"
        }

    else:
        mock_count_patient_radiographs.side_effect = mock_side_effect

    data = {
        **form_data,
        "file": (BytesIO(file_bytes), "uploaded_radiograph.png")
    }

    # Richiesta POST alla rotta /predict
    response = client.post("/predict", data=data, content_type="multipart/form-data")
    json_data = response.get_json()

    # Asserzioni
    assert response.status_code == expected_status_code, json_data
    if expected_status_code == 200:
        assert "original_image" in json_data
        assert "confidence" in json_data
        assert json_data["confidence"] == 0.87
    else:
        assert "error" in json_data
        assert expected_key_substring in json_data["error"]