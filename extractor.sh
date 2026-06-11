#!/usr/bin/env bash
set -euo pipefail

ZIP_URL="${1:-}"

if [ $# -ge 1 ]; then
    ZIP_URL="$1"
else
    read -rp "Enter ROM ZIP URL: " ZIP_URL
fi

if [ -z "$ZIP_URL" ]; then
    echo "No URL provided"
    exit 1
fi

for cmd in wget unzip brotli python3 curl debugfs; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Missing dependency: $cmd"
        exit 1
    fi
done

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"

echo "[*] Downloading ROM..."
wget -O rom.zip "$ZIP_URL"

echo "[*] Extracting ZIP..."
mkdir dump
unzip -q rom.zip -d dump
cd dump

if [ ! -f system.new.dat.br ]; then
    echo "system.new.dat.br not found"
    exit 1
fi

echo "[*] Decompressing system.new.dat.br..."
brotli --decompress system.new.dat.br
rm -f system.new.dat.br
echo "[*] Downloading sdat2img..."
curl -sLo sdat2img.py \
    https://raw.githubusercontent.com/xpirt/sdat2img/master/sdat2img.py

echo "[*] Converting DAT to IMG..."
python3 sdat2img.py \
    system.transfer.list \
    system.new.dat \
    system.img

echo "[*] Extracting build.prop from system.img..."

debugfs -R "dump /system/build.prop build.prop" system.img 2>/dev/null || \
debugfs -R "dump /build.prop build.prop" system.img 2>/dev/null || \
debugfs -R "dump /system/system/build.prop build.prop" system.img 2>/dev/null

if [ ! -f build.prop ]; then
    echo "[!] build.prop not found"

    echo
    echo "[*] Root directory:"
    debugfs -R "ls -p /" system.img 2>/dev/null || true

    echo
    echo "[*] /system directory:"
    debugfs -R "ls -p /system" system.img 2>/dev/null || true

    exit 1
fi

echo
echo "===== build.prop ====="
debugfs -R "ls -p /system/etc/permissions" system.img 2>/dev/null | grep -i fingerprint
debugfs -R "ls -p /system/etc/permissions" system.img 2>/dev/null | grep -i nfc
grep '^ro.product.system.marketname=' build.prop | cut -d= -f2-

rm -rf /tmp/tmp.*
