import pytest


@pytest.fixture
def lancamento(client, headers_admin, usuario_base, clifor_base, tipo_lancamento_base):
    r = client.post("/lancamento/", json={
        "id_usuario_fk_lancamento": usuario_base["id_usuario"],
        "id_clifor_relacionado_fk": clifor_base["id_clifor"],
        "id_tipo_lancamento_fk": tipo_lancamento_base["id_tipo_lancamento"],
        "valor": "250.00",
        "data_vencimento": "2026-12-31",
        "natureza_lancamento": "Debito",
        "observacao": "lancamento pytest"
    }, headers=headers_admin)
    data = r.json()
    yield data
    client.delete(f"/lancamento/{data['id_lancamento']}", headers=headers_admin)


def test_criar_lancamento(client, headers_admin, usuario_base, clifor_base, tipo_lancamento_base):
    r = client.post("/lancamento/", json={
        "id_usuario_fk_lancamento": usuario_base["id_usuario"],
        "id_clifor_relacionado_fk": clifor_base["id_clifor"],
        "id_tipo_lancamento_fk": tipo_lancamento_base["id_tipo_lancamento"],
        "valor": "100.00",
        "data_vencimento": "2026-06-30",
        "natureza_lancamento": "Credito"
    }, headers=headers_admin)
    assert r.status_code == 200
    data = r.json()
    client.delete(f"/lancamento/{data['id_lancamento']}", headers=headers_admin)


def test_criar_lancamento_sem_token(client, usuario_base, clifor_base, tipo_lancamento_base):
    r = client.post("/lancamento/", json={
        "id_usuario_fk_lancamento": usuario_base["id_usuario"],
        "id_clifor_relacionado_fk": clifor_base["id_clifor"],
        "id_tipo_lancamento_fk": tipo_lancamento_base["id_tipo_lancamento"],
        "valor": "50.00",
        "data_vencimento": "2026-01-01",
        "natureza_lancamento": "Debito"
    })
    assert r.status_code == 401


def test_listar_lancamentos(client, headers_admin):
    r = client.get("/lancamento/", headers=headers_admin)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_buscar_lancamento(client, headers_admin, lancamento):
    r = client.get(f"/lancamento/{lancamento['id_lancamento']}", headers=headers_admin)
    assert r.status_code == 200


def test_buscar_lancamento_inexistente(client, headers_admin):
    r = client.get("/lancamento/999999", headers=headers_admin)
    assert r.status_code == 404


def test_fechar_lancamento(client, headers_admin, lancamento, usuario_base):
    r = client.put(f"/lancamento/{lancamento['id_lancamento']}", json={
        "id_usuario_fk_fechamento": usuario_base["id_usuario"],
        "valor_pago": "250.00",
        "data_pagamento": "2026-04-21T00:00:00"
    }, headers=headers_admin)
    assert r.status_code == 200
    assert r.json()["valor_pago"] == "250.00"


def test_deletar_lancamento(client, headers_admin, usuario_base, clifor_base, tipo_lancamento_base):
    r = client.post("/lancamento/", json={
        "id_usuario_fk_lancamento": usuario_base["id_usuario"],
        "id_clifor_relacionado_fk": clifor_base["id_clifor"],
        "id_tipo_lancamento_fk": tipo_lancamento_base["id_tipo_lancamento"],
        "valor": "75.00",
        "data_vencimento": "2026-09-30",
        "natureza_lancamento": "Debito"
    }, headers=headers_admin)
    id_lanc = r.json()["id_lancamento"]
    r = client.delete(f"/lancamento/{id_lanc}", headers=headers_admin)
    assert r.status_code == 200
    r = client.get(f"/lancamento/{id_lanc}", headers=headers_admin)
    assert r.status_code == 404