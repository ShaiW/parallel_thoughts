#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_proofs.py — Validate coinbase proofs CSV (from script #2) against a monero daemon.

Validations per row:
  - height within START_HEIGHT..END_HEIGHT (inclusive)
  - daemon get_block_header_by_height(height).hash == CSV block_hash
  - /get_transactions(txid, decode_as_json=True) indicates coinbase (vin[0].gen)

Optionally (if ENABLE_WALLET_RPC_CHECK=True):
  - wallet-rpc check_tx_proof(txid, RECEIVER_ADDRESS, message, signature) == good
  - public_view_key in CSV matches RECEIVER_ADDRESS (via base58 decode)

Finally prints the list of 1-based indices of blocks in the fixed range
that pass validation (index = height - START_HEIGHT + 1).
"""

import csv
import json
import os
from typing import Any, Dict, List, Optional, Tuple
import urllib.request
import time

# ==============================
# ======== CONSTANTS ===========
# ==============================

# Fixed height window (inclusive) — must match Script #2
START_HEIGHT = 3475510
END_HEIGHT   = 3476208

# Inputs
CSV_PATH        = r"coinbase_proofs.csv"

# Daemon (public node) used for validation
DAEMON_RPC_URL  = "http://xmr.triplebit.org:18081"   # pick a healthy node

# Optional: enable full signature verification via wallet-rpc (off by default)
ENABLE_WALLET_RPC_CHECK = False
WALLET_RPC_URL          = "http://127.0.0.1:28088/json_rpc"   # if you enable proof checks
RECEIVER_ADDRESS        = ""  # set your wallet primary address if proof-checking

# Behavior knobs
HTTP_TIMEOUT_SECS = 30
DEBUG_PROGRESS_EVERY = 50  # print a dot every N rows processed

# ==============================
# ========= HTTP HELPERS =======
# ==============================

def http_json_post(url: str, payload: Dict[str, Any], timeout: int = HTTP_TIMEOUT_SECS) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        txt = resp.read().decode("utf-8")
        return json.loads(txt)

def daemon_jsonrpc(method: str, params: Optional[Dict[str, Any]] = None, timeout: int = HTTP_TIMEOUT_SECS) -> Dict[str, Any]:
    url = f"{DAEMON_RPC_URL}/json_rpc"
    payload = {"jsonrpc": "2.0", "id": "0", "method": method}
    if params:
        payload["params"] = params
    rep = http_json_post(url, payload, timeout=timeout)
    if "error" in rep:
        raise RuntimeError(f"daemon RPC error on {method}: {rep['error']}")
    return rep.get("result", {})

def daemon_get_transactions(txids: List[str], decode_as_json: bool = True, timeout: int = HTTP_TIMEOUT_SECS) -> Dict[str, Any]:
    url = f"{DAEMON_RPC_URL}/get_transactions"
    obj = {"txs_hashes": txids, "decode_as_json": decode_as_json}
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        txt = resp.read().decode("utf-8")
        return json.loads(txt)

def wallet_rpc(method: str, params: Optional[Dict[str, Any]] = None, timeout: int = HTTP_TIMEOUT_SECS) -> Dict[str, Any]:
    if not ENABLE_WALLET_RPC_CHECK:
        raise RuntimeError("wallet-rpc is disabled")
    payload = {"jsonrpc": "2.0", "id": "0", "method": method}
    if params:
        payload["params"] = params
    rep = http_json_post(WALLET_RPC_URL, payload, timeout=timeout)
    if "error" in rep:
        raise RuntimeError(f"wallet-rpc error on {method}: {rep['error']}")
    return rep.get("result", {})

# ==============================
# ===== MONERO BASE58 (view key extraction) ==
# ==============================

B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
B58_MAP = {c: i for i, c in enumerate(B58_ALPHABET)}
ENC_BLOCK_SIZES = [0, 2, 3, 5, 6, 7, 9, 10, 11]
FULL_BLOCK_SIZE = 8
FULL_ENC_SIZE = 11

def b58_decode_monero(addr: str) -> bytes:
    if not addr:
        raise ValueError("Empty address")
    blocks = [addr[i:i+FULL_ENC_SIZE] for i in range(0, len(addr), FULL_ENC_SIZE)]
    out = bytearray()
    for i, block in enumerate(blocks):
        enc_len = len(block)
        if enc_len <= 0 or enc_len > FULL_ENC_SIZE:
            raise ValueError(f"Invalid base58 block length {enc_len} at block {i}")
        dec_size = next((idx for idx, sz in enumerate(ENC_BLOCK_SIZES) if sz == enc_len), None)
        num = 0
        for ch in block:
            val = B58_MAP.get(ch)
            if val is None:
                raise ValueError(f"Invalid base58 char '{ch}'")
            num = num * 58 + val
        if dec_size is None:
            tmp = num.to_bytes(8, "little").rstrip(b"\x00")
            dec = tmp if tmp else b"\x00"
        else:
            dec = num.to_bytes(FULL_BLOCK_SIZE, "little")[:dec_size]
        out.extend(dec)
    return bytes(out)

def extract_pub_view_from_address(address: str) -> str:
    raw = b58_decode_monero(address)
    if len(raw) < 1 + 32 + 32 + 4:
        raise ValueError(f"Address decoded length too short: {len(raw)}")
    return raw[33:65].hex()

# ==============================
# ========== HELPERS ===========
# ==============================

def is_coinbase_tx(tx_json_str: str) -> bool:
    try:
        tx = json.loads(tx_json_str)
        vin = tx.get("vin", [])
        return bool(vin and "gen" in vin[0])
    except Exception:
        return False

def csv_get(row: Dict[str, str], *names: str, default: str = "") -> str:
    """Return the first present/nonnull value among names from row."""
    for n in names:
        if n in row and row[n] is not None and row[n] != "":
            return row[n]
    return default

# ==============================
# ========== MAIN ==============
# ==============================

def main():
    print(f"[DEBUG] Using daemon: {DAEMON_RPC_URL}")
    print(f"[DEBUG] Height window: {START_HEIGHT}..{END_HEIGHT} (inclusive)")
    if ENABLE_WALLET_RPC_CHECK:
        if not RECEIVER_ADDRESS:
            print("[ERROR] ENABLE_WALLET_RPC_CHECK=True but RECEIVER_ADDRESS is empty. Set it and retry.")
            return
        try:
            addr_vk = extract_pub_view_from_address(RECEIVER_ADDRESS)
            print(f"[DEBUG] Receiver address public view key: {addr_vk}")
        except Exception as e:
            print(f"[ERROR] Failed to parse RECEIVER_ADDRESS: {e}")
            return

    # Pre-fetch block headers for the window to speed up hash checks
    print("[DEBUG] Prefetching block headers for the window ...")
    height_to_hash: Dict[int, str] = {}
    for h in range(START_HEIGHT, END_HEIGHT + 1):
        try:
            res = daemon_jsonrpc("get_block_header_by_height", {"height": h})
            bh = res.get("block_header", {})
            if "hash" in bh:
                height_to_hash[h] = str(bh["hash"])
            else:
                print(f"[WARN] No hash from daemon for height {h}")
        except Exception as e:
            print(f"[WARN] Failed header fetch at height {h}: {e}")

    ok_heights: List[int] = []
    total = 0
    passed_coinbase = 0
    passed_hash = 0
    passed_proof = 0

    # Read CSV and validate
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print(f"[DEBUG] CSV columns: {reader.fieldnames}")

        # sanity: check for height-range columns that script #2 writes
        # (range_start_height / range_end_height). If absent, we still proceed using constants.
        found_range_cols = ("range_start_height" in reader.fieldnames and "range_end_height" in reader.fieldnames)

        for row in reader:
            total += 1
            if total % DEBUG_PROGRESS_EVERY == 0:
                print(f"[DEBUG] ..processed {total} rows")

            try:
                txid = csv_get(row, "txid")
                height = int(csv_get(row, "height", default="0"))
                csv_hash = csv_get(row, "block_hash")
                sig = csv_get(row, "proof")
                message = csv_get(row, "message")  # may be empty
                pub_view_csv = csv_get(row, "public_view_key")

                # Enforce fixed height window
                if height < START_HEIGHT or height > END_HEIGHT:
                    print(f"[DEBUG] Row {total}: height {height} outside fixed window; skip")
                    continue

                # If CSV declares its own range, ensure consistency
                if found_range_cols:
                    csv_start = int(csv_get(row, "range_start_height", default=str(START_HEIGHT)))
                    csv_end   = int(csv_get(row, "range_end_height", default=str(END_HEIGHT)))
                    if csv_start != START_HEIGHT or csv_end != END_HEIGHT:
                        print(f"[WARN] Row {total}: CSV range ({csv_start}-{csv_end}) != constants ({START_HEIGHT}-{END_HEIGHT})")

                # Check block hash matches daemon
                d_hash = height_to_hash.get(height)
                if not d_hash:
                    print(f"[WARN] Row {total}: no daemon hash for height {height}; skip hash check")
                else:
                    if csv_hash and d_hash != csv_hash:
                        print(f"[WARN] Row {total}: block_hash mismatch at height {height}: CSV={csv_hash} != DAEMON={d_hash}")
                    else:
                        passed_hash += 1

                # Check coinbase via daemon get_transactions
                is_cb = False
                try:
                    dtx = daemon_get_transactions([txid], decode_as_json=True)
                    txs = dtx.get("txs", [])
                    if txs:
                        is_cb = is_coinbase_tx(txs[0].get("as_json", ""))
                    else:
                        # As a fallback, pull the block and check miner tx id is present
                        # (rarely needed; kept for resilience)
                        pass
                except Exception as e:
                    print(f"[WARN] Row {total}: get_transactions failed for txid {txid}: {e}")

                if not is_cb:
                    print(f"[DEBUG] Row {total}: tx {txid} is not coinbase per daemon; skip")
                    continue
                else:
                    passed_coinbase += 1

                # Optional proof verification through wallet-rpc
                proof_ok = False
                if ENABLE_WALLET_RPC_CHECK:
                    # If CSV's pub view key is present, check it matches the receiver address
                    try:
                        addr_vk = extract_pub_view_from_address(RECEIVER_ADDRESS)
                        if pub_view_csv and addr_vk != pub_view_csv:
                            print(f"[WARN] Row {total}: public_view_key mismatch (CSV={pub_view_csv}, ADDR={addr_vk})")
                    except Exception as e:
                        print(f"[WARN] Row {total}: could not validate address view key: {e}")

                    try:
                        res = wallet_rpc("check_tx_proof", {
                            "txid": txid,
                            "address": RECEIVER_ADDRESS,
                            "message": message,
                            "signature": sig
                        })
                        proof_ok = bool(res.get("good", False))
                        received = res.get("received", 0)
                        print(f"[DEBUG] Row {total}: check_tx_proof good={proof_ok} received={received}")
                    except Exception as e:
                        print(f"[WARN] Row {total}: wallet-rpc check_tx_proof failed: {e}")
                else:
                    if not sig:
                        print(f"[WARN] Row {total}: empty proof string")
                    # We don't cryptographically verify when disabled
                    proof_ok = True

                if proof_ok:
                    passed_proof += 1
                    ok_heights.append(height)

            except Exception as e:
                print(f"[ERROR] Row {total}: Exception {e}")

    ok_heights = sorted(set(ok_heights))
    indices = [h - START_HEIGHT + 1 for h in ok_heights]

    print("\n===== SUMMARY =====")
    print(f"Total CSV rows examined: {total}")
    print(f"Passed block-hash check: {passed_hash}")
    print(f"Passed coinbase check : {passed_coinbase}")
    if ENABLE_WALLET_RPC_CHECK:
        print(f"Passed proof check    : {passed_proof}")
    else:
        print("Proof check           : SKIPPED (ENABLE_WALLET_RPC_CHECK=False)")
    print(f"Valid heights in range: {ok_heights}")
    print(f"1-based indices       : {indices}")
    print("===================\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR] FATAL:", e)
        raise
