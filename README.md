# simulação_ataque_força_bruta

## O que contém este repositório

- `README.md` este arquivo, com instruções.
- `wordlists/` lista de palavras exemplo (pequenas) para FTP/SMB.
- `scripts/` scripts para automatizar ataques com Medusa e um script Python para brute-force em formulários (DVWA).
- `images/` pasta para capturas de tela (opcional).

## Cenários

1. FTP (Metasploitable 2) força bruta de credenciais FTP com Medusa.
2. DVWA (web) automação de tentativas em formulário web.
3. SMB (Metasploitable 2) password spraying com enumeração de usuários.

## Requisitos

- VirtualBox com duas VMs: Kali Linux e Metasploitable 2 (ou DVWA).  
- Rede: host-only ou internal network (para isolar o laboratório).  
- Na Kali: `medusa` instalado (`sudo apt update && sudo apt install medusa -y`).  
- Python 3 + requests (para o script DVWA): `python3 -m pip install requests`

Use a mesma rede host-only nas duas VMs. Ajuste IPs conforme sua configuração.

## Preparação das VMs

1. Inicie a VM Metasploitable 2 (padrões: usuário `msfadmin` / senha `msfadmin`).
2. Inicie a VM Kali.
3. Verifique o ip do Metasploitable 2 (digite no terminal `ifconfig`).

## Medusa — exemplos práticos

Observação: execute os comandos no Kali.

1) Força bruta FTP (arquivo de usuários e senhas):

Exemplo:
medusa -h 192.168.56.20 -U wordlists/users.txt -P wordlists/passwords.txt -M ftp -t 4 -f

- `-h` alvo, `-U` lista de usuários, `-P` lista de senhas, `-M ftp` módulo FTP, `-t` threads, `-f` parar ao encontrar credenciais válidas.

2) Password spraying SMB (uma senha, vários usuários):

Exemplo:
medusa -h 192.168.56.20 -U wordlists/users.txt -p 'Password123' -M smbnt -t 4 -f

3) Dica 
- Para testes longos, redirecione a saída para um arquivo e analise os resultados mais tarde.

## Scripts

Veja `scripts/` para ferramentas de automação. Exemplos incluídos:

- `scripts/medusa_ftp.sh` — wrapper que recebe alvo, arquivo de usuários e arquivo de senhas.
- `scripts/medusa_smb.sh` — wrapper para password spraying em SMB (alvo, arquivo de usuários, senha única).
- `scripts/dvwa_bruteforce.py` — script Python que automatiza login em formulário DVWA; tenta extrair token CSRF se presente.

Use `chmod +x scripts/*.sh` antes de executar os `.sh`.

### Exemplo de uso do script Python (DVWA)

```bash
# Instale a dependência requests (na Kali)
python3 -m pip install requests

# Execute o script (ajuste parâmetros conforme necessário)
python3 scripts/dvwa_bruteforce.py --url http://192.168.56.20 --usuarios wordlists/users.txt --senhas wordlists/passwords.txt
```

**Parâmetros disponíveis:**
- `--url` URL base do DVWA (obrigatório)
- `--caminho-login` caminho do formulário de login (padrão: `/login.php`)
- `--usuarios` arquivo com nomes de usuário, um por linha (obrigatório)
- `--senhas` arquivo com senhas, uma por linha (obrigatório)
- `--delay` atraso entre tentativas em segundos (padrão: 0.2)

## Wordlists de exemplo

As listas em `wordlists/` são pequenas e servem apenas como exemplo. Para testes mais reais, use wordlists maiores como as do SecLists.

## DVWA — notas sobre brute-force em formulário

DVWA tem níveis de segurança. Para praticar brute-force via script HTTP, configure o nível para "low" no painel de DVWA (isso desativa tokens que complicam a automação). O script em `scripts/dvwa_bruteforce.py` tenta detectar um token (`user_token`) e inclui-lo se encontrado.

# simulação_ataque_força_bruta

