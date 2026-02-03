import requests
import pandas as pd
import re
import time

# Header obrigatório para o Nominatim
HEADERS = {
    "User-Agent": "ConsultaCEP/1.0 (contato@exemplo.com)"
}

# ---------- VALIDAÇÃO DE CEP ----------

def validar_formato_cep(cep):
    """Remove caracteres não numéricos e valida tamanho"""
    cep_limpo = re.sub(r"\D", "", cep)
    return cep_limpo if len(cep_limpo) == 8 else None

def validar_cep_viacep(cep):
    """Verifica se o CEP existe usando a API ViaCEP"""
    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url, timeout=10)
        data = response.json()
        return not data.get("erro", False)
    except requests.RequestException:
        return False

def validar_cep(cep):
    """Validação completa do CEP"""
    cep_limpo = validar_formato_cep(cep)
    if not cep_limpo:
        return None

    if validar_cep_viacep(cep_limpo):
        return cep_limpo

    return None

# ---------- GEOLOCALIZAÇÃO ----------

def get_lat_lon_by_cep(cep):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": cep,
        "format": "json",
        "countrycodes": "BR"
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            return None, None

    except requests.RequestException as e:
        print(f"Erro ao consultar geolocalização do CEP {cep}: {e}")
        return None, None

# ---------- COLETA DE DADOS ----------

def get_data(ceps):
    dados = {
        "CEP": [],
        "Latitude": [],
        "Longitude": []
    }

    for cep in ceps:
        print(f"Consultando CEP válido: {cep}")
        lat, lon = get_lat_lon_by_cep(cep)

        dados["CEP"].append(cep)
        dados["Latitude"].append(lat)
        dados["Longitude"].append(lon)

        time.sleep(1)  # respeita limite da API

    return dados

# ---------- SALVAR EXCEL ----------

def save_to_excel(data, filename="dados_ceps.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"\nArquivo Excel gerado com sucesso: {filename}")

# ---------- MAIN ----------

if __name__ == "__main__":
    entrada = input("Digite os CEPs separados por vírgula: ")
    ceps_input = [cep.strip() for cep in entrada.split(",")]

    ceps_validos = []

    for cep in ceps_input:
        cep_validado = validar_cep(cep)
        if cep_validado:
            ceps_validos.append(cep_validado)
        else:
            print(f"CEP inválido ignorado: {cep}")

    if ceps_validos:
        data = get_data(ceps_validos)
        save_to_excel(data)
    else:
        print("Nenhum CEP válido informado.")
