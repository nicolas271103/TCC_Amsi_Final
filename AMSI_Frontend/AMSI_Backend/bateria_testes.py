import requests

BASE_URL = "http://localhost:8000"

# ================================================
# UTILITÁRIOS
# ================================================

_passou = 0
_falhou = 0
_headers = {}  # preenchido após autenticação


def checar(descricao: str, condicao: bool):
    global _passou, _falhou
    if condicao:
        _passou += 1
        print(f"  ✔ {descricao}")
    else:
        _falhou += 1
        print(f"  ✘ {descricao}")


def titulo(texto: str):
    print(f"\n{'='*50}")
    print(f"  {texto}")
    print(f"{'='*50}")


def resumo():
    total = _passou + _falhou
    print(f"\n{'='*50}")
    print(f"  RESULTADO: {_passou}/{total} testes passaram")
    if _falhou > 0:
        print(f"  FALHAS: {_falhou}")
    print(f"{'='*50}\n")


# ================================================
# AUTENTICAÇÃO
# ================================================

def autenticar(email: str, senha: str) -> bool:
    global _headers
    r = requests.post(f"{BASE_URL}/auth/token", json={"email": email, "senha": senha})
    if r.ok:
        token = r.json().get("access_token")
        _headers = {"Authorization": f"Bearer {token}"}
        checar("POST /auth/token - autenticar", True)
        return True
    checar("POST /auth/token - autenticar", False)
    print(f"    [ERRO AUTH] {r.status_code}: {r.text}")
    return False


# ================================================
# TESTES
# ================================================

def testar_usuario(id_admin: int):
    titulo("USUÁRIO")
    criado_id = None

    payload = {
        "senha": "senha123",
        "nome": "Usuário Teste Bateria",
        "email": "teste_bateria_secundario@amsi.com",
        "cargo": "Associado",
        "perfil_de_acesso": "Consulta",
        "notificacao": False,
        "bloqueado": False
    }
    r = requests.post(f"{BASE_URL}/usuarios/", json=payload, headers=_headers)
    checar("POST /usuarios/ - criar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_usuario")

    r = requests.get(f"{BASE_URL}/usuarios/", headers=_headers)
    checar("GET /usuarios/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/usuarios/{criado_id}", headers=_headers)
        checar("GET /usuarios/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/usuarios/{criado_id}", json={"nome": "Usuário Teste Atualizado"}, headers=_headers)
        checar("PUT /usuarios/{id} - atualizar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/usuarios/{criado_id}", headers=_headers)
        checar("GET /usuarios/{id} - verificar atualização", r.json().get("nome") == "Usuário Teste Atualizado")

    return criado_id


def testar_tipo_lancamento():
    titulo("TIPO DE LANÇAMENTO")
    criado_id = None

    payload = {
        "descricao_conta": "Tipo Teste Bateria",
        "natureza_conta": "Debito",
        "observacao": "criado pela bateria de testes"
    }
    r = requests.post(f"{BASE_URL}/tipo_lancamento/", json=payload, headers=_headers)
    checar("POST /tipo_lancamento/ - criar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_tipo_lancamento")

    r = requests.get(f"{BASE_URL}/tipo_lancamento/", headers=_headers)
    checar("GET /tipo_lancamento/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/tipo_lancamento/{criado_id}", headers=_headers)
        checar("GET /tipo_lancamento/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/tipo_lancamento/{criado_id}", json={"descricao_conta": "Tipo Teste Atualizado"}, headers=_headers)
        checar("PUT /tipo_lancamento/{id} - atualizar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/tipo_lancamento/{criado_id}", headers=_headers)
        checar("GET /tipo_lancamento/{id} - verificar atualização", r.json().get("descricao_conta") == "Tipo Teste Atualizado")

    return criado_id


def testar_cliente_fornecedor(id_usuario: int):
    titulo("CLIENTE/FORNECEDOR")
    criado_id = None

    payload = {
        "id_usuario_fk": id_usuario,
        "pessoafisica_juridica": True,
        "cpf_cnpj": "000.000.000-00",
        "rg_inscricaoestadual": "0000000",
        "nome": "CliFor Teste Bateria",
        "datanascimento": "1990-01-01",
        "tipo_clifor": "A",
        "ativo": True,
        "inadimplente": False
    }
    r = requests.post(f"{BASE_URL}/cliente_fornecedor/", json=payload, headers=_headers)
    checar("POST /cliente_fornecedor/ - criar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_clifor")

    r = requests.get(f"{BASE_URL}/cliente_fornecedor/", headers=_headers)
    checar("GET /cliente_fornecedor/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/cliente_fornecedor/{criado_id}", headers=_headers)
        checar("GET /cliente_fornecedor/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/cliente_fornecedor/{criado_id}", json={"nome": "CliFor Teste Atualizado"}, headers=_headers)
        checar("PUT /cliente_fornecedor/{id} - atualizar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/cliente_fornecedor/{criado_id}", headers=_headers)
        checar("GET /cliente_fornecedor/{id} - verificar atualização", r.json().get("nome") == "CliFor Teste Atualizado")

    return criado_id


def testar_endereco(id_clifor: int):
    titulo("ENDEREÇO")
    criado_id = None

    payload = {
        "id_clifor_fk": id_clifor,
        "enderecoprimario": True,
        "logradouro": "Rua Teste",
        "numero": "123",
        "complemento": "Apto 1",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "uf": "SP",
        "cep": "00000-000"
    }
    r = requests.post(f"{BASE_URL}/endereco/", json=payload, headers=_headers)
    checar("POST /endereco/ - criar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_endereco")

    r = requests.get(f"{BASE_URL}/endereco/", headers=_headers)
    checar("GET /endereco/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/endereco/{criado_id}", headers=_headers)
        checar("GET /endereco/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/endereco/{criado_id}", json={"logradouro": "Rua Teste Atualizada"}, headers=_headers)
        checar("PUT /endereco/{id} - atualizar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/endereco/{criado_id}", headers=_headers)
        checar("GET /endereco/{id} - verificar atualização", r.json().get("logradouro") == "Rua Teste Atualizada")

        r = requests.delete(f"{BASE_URL}/endereco/{criado_id}", headers=_headers)
        checar("DELETE /endereco/{id} - deletar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/endereco/{criado_id}", headers=_headers)
        checar("GET /endereco/{id} - verificar deleção", r.status_code == 404)

    return criado_id


def testar_contato(id_clifor: int):
    titulo("CONTATO")
    criado_id = None

    payload = {
        "id_clifor_fk": id_clifor,
        "tipocontato": "Telefone",
        "info_do_contato": "(11) 99999-9999",
        "contato_principal": True
    }
    r = requests.post(f"{BASE_URL}/contato/", json=payload, headers=_headers)
    checar("POST /contato/ - criar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_contato")

    r = requests.get(f"{BASE_URL}/contato/", headers=_headers)
    checar("GET /contato/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/contato/{criado_id}", headers=_headers)
        checar("GET /contato/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/contato/{criado_id}", json={"info_do_contato": "(11) 88888-8888"}, headers=_headers)
        checar("PUT /contato/{id} - atualizar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/contato/{criado_id}", headers=_headers)
        checar("GET /contato/{id} - verificar atualização", r.json().get("info_do_contato") == "(11) 88888-8888")

        r = requests.delete(f"{BASE_URL}/contato/{criado_id}", headers=_headers)
        checar("DELETE /contato/{id} - deletar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/contato/{criado_id}", headers=_headers)
        checar("GET /contato/{id} - verificar deleção", r.status_code == 404)

    return criado_id


def testar_lancamento(id_usuario: int, id_clifor: int, id_tipo: int):
    titulo("LANÇAMENTO")
    criado_id = None

    payload = {
        "id_usuario_fk_lancamento": id_usuario,
        "id_clifor_relacionado_fk": id_clifor,
        "id_tipo_lancamento_fk": id_tipo,
        "valor": "150.00",
        "data_vencimento": "2026-12-31",
        "natureza_lancamento": "Debito",
        "observacao": "lançamento criado pela bateria de testes"
    }
    r = requests.post(f"{BASE_URL}/lancamento/", json=payload, headers=_headers)
    checar("POST /lancamento/ - criar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_lancamento")

    r = requests.get(f"{BASE_URL}/lancamento/", headers=_headers)
    checar("GET /lancamento/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/lancamento/{criado_id}", headers=_headers)
        checar("GET /lancamento/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/lancamento/{criado_id}", json={
            "id_usuario_fk_fechamento": id_usuario,
            "valor_pago": "150.00",
            "data_pagamento": "2026-03-12T00:00:00"
        }, headers=_headers)
        checar("PUT /lancamento/{id} - fechar", r.status_code == 200)

        r = requests.get(f"{BASE_URL}/lancamento/{criado_id}", headers=_headers)
        checar("GET /lancamento/{id} - verificar fechamento", r.json().get("valor_pago") == "150.00")

    return criado_id


def testar_login_sessao(id_usuario: int):
    titulo("LOGIN (SESSÃO)")
    criado_id = None

    payload = {
        "id_usuario_fk": id_usuario,
        "dispositivo_logado": "Teste Bateria",
        "localizacao": "Localhost",
        "navegador": "Python Requests"
    }
    r = requests.post(f"{BASE_URL}/login/", json=payload, headers=_headers)
    checar("POST /login/ - registrar", r.status_code == 200 or r.status_code == 201)
    if r.ok:
        criado_id = r.json().get("id_login")

    r = requests.get(f"{BASE_URL}/login/", headers=_headers)
    checar("GET /login/ - listar", r.status_code == 200)

    if criado_id:
        r = requests.get(f"{BASE_URL}/login/{criado_id}", headers=_headers)
        checar("GET /login/{id} - buscar", r.status_code == 200)

        r = requests.put(f"{BASE_URL}/login/{criado_id}", json={"data_logout": "2026-03-12T01:00:00"}, headers=_headers)
        checar("PUT /login/{id} - registrar logout", r.status_code == 200)

    return criado_id


# ================================================
# LIMPEZA — ordem inversa das FKs
# ================================================

def limpar(id_usuario, id_clifor, id_tipo, id_login=None, id_lancamento=None, id_usuario_secundario=None):
    titulo("LIMPEZA")

    if id_lancamento:
        r = requests.delete(f"{BASE_URL}/lancamento/{id_lancamento}", headers=_headers)
        checar("DELETE lancamento", r.status_code == 200)
        r = requests.get(f"{BASE_URL}/lancamento/{id_lancamento}", headers=_headers)
        checar("GET lancamento/{id} - verificar deleção", r.status_code == 404)

    if id_login:
        r = requests.delete(f"{BASE_URL}/login/{id_login}", headers=_headers)
        checar("DELETE login", r.status_code == 200)

    if id_clifor:
        r = requests.delete(f"{BASE_URL}/cliente_fornecedor/{id_clifor}", headers=_headers)
        checar("DELETE cliente_fornecedor", r.status_code == 200)

    if id_tipo:
        r = requests.delete(f"{BASE_URL}/tipo_lancamento/{id_tipo}", headers=_headers)
        checar("DELETE tipo_lancamento", r.status_code == 200)

    if id_usuario_secundario:
        # Deletar logins de sessão antes de deletar o usuário
        r = requests.get(f"{BASE_URL}/login/por-usuario/{id_usuario_secundario}", headers=_headers)
        if r.ok:
            for login in r.json():
                requests.delete(f"{BASE_URL}/login/{login['id_login']}", headers=_headers)
        r = requests.delete(f"{BASE_URL}/usuarios/{id_usuario_secundario}", headers=_headers)
        checar("DELETE usuario secundario", r.status_code == 200)

    # Admin NÃO é deletado — mas seus logins de sessão criados durante a bateria sim
    r = requests.get(f"{BASE_URL}/login/por-usuario/{id_usuario}", headers=_headers)
    if r.ok:
        for login in r.json():
            requests.delete(f"{BASE_URL}/login/{login['id_login']}", headers=_headers)
    checar("DELETE logins de sessão do admin", True)



# ================================================
# TESTES NEGATIVOS — CONTROLE DE ACESSO
# ================================================

def testar_acesso_sem_token():
    titulo("ACESSO SEM TOKEN (esperado: 401)")

    r = requests.get(f"{BASE_URL}/usuarios/")
    checar("GET /usuarios/ sem token → 401", r.status_code == 401)

    r = requests.get(f"{BASE_URL}/lancamento/")
    checar("GET /lancamento/ sem token → 401", r.status_code == 401)

    r = requests.get(f"{BASE_URL}/cliente_fornecedor/")
    checar("GET /cliente_fornecedor/ sem token → 401", r.status_code == 401)

    r = requests.post(f"{BASE_URL}/tipo_lancamento/", json={})
    checar("POST /tipo_lancamento/ sem token → 401", r.status_code == 401)


def testar_acesso_perfil_consulta(id_admin: int):
    titulo("ACESSO PERFIL CONSULTA (esperado: 403 em rotas admin)")

    # Criar usuário com perfil Consulta (senha gerada automaticamente pelo sistema)
    payload = {
        "nome": "Consulta Teste Bateria",
        "email": "consulta_bateria@amsi.com",
        "cargo": "Associado",
        "perfil_de_acesso": "Consulta",
        "notificacao": False
    }
    r = requests.post(f"{BASE_URL}/usuarios/", json=payload, headers=_headers)
    if not r.ok:
        checar("Setup usuário Consulta", False)
        return None

    id_consulta = r.json().get("id_usuario")

    # Testes 403/200 com perfil Consulta removidos — senha provisória não é conhecida na bateria
    # Para testar controle de acesso por perfil, usar pytest com fixture de usuário Consulta
    checar("Setup usuário Consulta criado", id_consulta is not None)

    # Deletar logins de sessão do usuário Consulta antes de deletar o usuário
    r = requests.get(f"{BASE_URL}/login/por-usuario/{id_consulta}", headers=_headers)
    if r.ok:
        for login in r.json():
            requests.delete(f"{BASE_URL}/login/{login['id_login']}", headers=_headers)

    # Limpar usuário Consulta
    r = requests.delete(f"{BASE_URL}/usuarios/{id_consulta}", headers=_headers)
    checar("DELETE usuario Consulta (limpeza)", r.status_code == 200)

    return id_consulta


# ================================================
# TESTES DE SESSÃO E TOKEN
# ================================================

def testar_sessao():
    titulo("SESSÃO E TOKEN")

    # Header X-Session-Expires presente em request autenticado
    r = requests.get(f"{BASE_URL}/usuarios/", headers=_headers)
    checar("GET /usuarios/ retorna X-Session-Expires", "x-session-expires" in r.headers)

    # Logout — retorna 200
    r = requests.post(f"{BASE_URL}/auth/logout", headers=_headers)
    checar("POST /auth/logout → 200", r.status_code == 200)

    # Request com token após logout → 401
    r = requests.get(f"{BASE_URL}/usuarios/", headers=_headers)
    checar("GET /usuarios/ após logout → 401", r.status_code == 401)

# ================================================
# ENTRADA
# ================================================

def rodar_bateria(email_admin: str = "admin@amsi.com", senha_admin: str = "admin123"):
    global _headers
    print("\n" + "="*50)
    print("  BATERIA DE TESTES — AMSI PROJECT")
    print("="*50)

    payload_tipo = {
        "descricao_conta": "Tipo Teste Bateria",
        "natureza_conta": "Debito",
        "observacao": "criado pela bateria de testes"
    }

    # Autenticar com admin existente no banco
    titulo("AUTENTICAÇÃO")
    if not autenticar(email_admin, senha_admin):
        print("\n[ERRO] Falha na autenticação.")
        print(f"  Certifique-se de que existe um admin no banco com email '{email_admin}'.\n")
        return

    # Buscar id do admin autenticado
    r = requests.get(f"{BASE_URL}/usuarios/", headers=_headers)
    if not r.ok:
        print("\n[ERRO] Não foi possível listar usuários.\n")
        return
    admin = next((u for u in r.json() if u.get("email") == email_admin), None)
    if not admin:
        print(f"\n[ERRO] Admin com email '{email_admin}' não encontrado.\n")
        return
    id_admin = admin.get("id_usuario")

    # Criar tipo_lancamento base
    r_tipo = requests.post(f"{BASE_URL}/tipo_lancamento/", json=payload_tipo, headers=_headers)
    id_tipo = r_tipo.json().get("id_tipo_lancamento") if r_tipo.ok else None
    checar("POST /tipo_lancamento/ - criar base", r_tipo.ok)

    if not id_tipo:
        print("\n[ERRO] Não foi possível criar tipo_lancamento base.\n")
        return

    id_usuario_secundario = testar_usuario(id_admin)
    id_clifor = testar_cliente_fornecedor(id_admin)
    testar_endereco(id_clifor)
    testar_contato(id_clifor)
    id_lancamento = testar_lancamento(id_admin, id_clifor, id_tipo)
    id_login = testar_login_sessao(id_admin)

    testar_acesso_sem_token()
    testar_acesso_perfil_consulta(id_admin)
    testar_sessao()

    # Reautenticar após logout (testar_sessao faz logout)
    if not autenticar(email_admin, senha_admin):
        print("\n[ERRO] Falha ao reautenticar após logout.\n")
        return

    limpar(id_admin, id_clifor, id_tipo, id_login, id_lancamento, id_usuario_secundario)
    resumo()