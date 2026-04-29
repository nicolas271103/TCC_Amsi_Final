import pytest


@pytest.fixture
def clifor(client, headers_admin, usuario_base):
    r = client.post("/cliente_fornecedor/", json={
        "id_usuario_fk": usuario_base["id_usuario"],
        "pessoafisica_juridica": True,
        "cpf_cnpj": "222.222.222-22",
        "rg_inscricaoestadual": "2222222",
        "nome": "CliFor Pytest Fixture",
        "datanascimento": "1985-06-15",
        "tipo_clifor": "C",
        "ativo": True,
        "inadimplente": False
    }, headers=headers_admin)
    data = r.json()
    yield data
    client.delete(f"/cliente_fornecedor/{data['id_clifor']}", headers=headers_admin)


def test_criar_clifor(client, headers_admin, usuario_base):
    r = client.post("/cliente_fornecedor/", json={
        "id_usuario_fk": usuario_base["id_usuario"],
        "pessoafisica_juridica": False,
        "cpf_cnpj": "33.333.333/0001-33",
        "rg_inscricaoestadual": "333333333",
        "nome": "CliFor Pytest Temp",
        "datanascimento": "2000-01-01",
        "tipo_clifor": "F",
        "ativo": True,
        "inadimplente": False
    }, headers=headers_admin)
    assert r.status_code == 200
    data = r.json()
    client.delete(f"/cliente_fornecedor/{data['id_clifor']}", headers=headers_admin)


def test_criar_clifor_sem_token(client, usuario_base):
    r = client.post("/cliente_fornecedor/", json={
        "id_usuario_fk": usuario_base["id_usuario"],
        "pessoafisica_juridica": True,
        "cpf_cnpj": "000.000.000-00",
        "rg_inscricaoestadual": "0000000",
        "nome": "Sem Token",
        "datanascimento": "1990-01-01",
        "tipo_clifor": "A",
        "ativo": True,
        "inadimplente": False
    })
    assert r.status_code == 401


def test_listar_clifors(client, headers_admin):
    r = client.get("/cliente_fornecedor/", headers=headers_admin)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_buscar_clifor(client, headers_admin, clifor):
    r = client.get(f"/cliente_fornecedor/{clifor['id_clifor']}", headers=headers_admin)
    assert r.status_code == 200


def test_buscar_clifor_inexistente(client, headers_admin):
    r = client.get("/cliente_fornecedor/999999", headers=headers_admin)
    assert r.status_code == 404


def test_atualizar_clifor(client, headers_admin, clifor):
    r = client.put(f"/cliente_fornecedor/{clifor['id_clifor']}",
                   json={"nome": "CliFor Atualizado"},
                   headers=headers_admin)
    assert r.status_code == 200
    assert r.json()["nome"] == "CliFor Atualizado"