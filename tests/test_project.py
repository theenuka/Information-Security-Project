from chaos_aes.aes_core import AES128
from chaos_aes.aes_tables import S_BOX
from chaos_aes.chaos_sbox import make_sbox
from chaos_aes.metrics import analyze_sbox
from chaos_aes.optimized_sbox import make_optimized_sbox


def test_standard_aes_known_vector():
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    ct = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
    assert AES128(key).encrypt_block(pt) == ct


def test_dynamic_roundtrip():
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    pt = b"sixteen byte txt"
    for sbox in [make_sbox(key), make_optimized_sbox()]:
        aes = AES128(key, sbox)
        assert aes.decrypt_block(aes.encrypt_block(pt)) == pt


def test_optimized_preserves_core_aes_sbox_strength():
    base, opt = analyze_sbox(S_BOX), analyze_sbox(make_optimized_sbox())
    assert opt["nonlinearity"] == base["nonlinearity"]
    assert opt["differential_uniformity"] == base["differential_uniformity"]
    assert opt["sac_error"] < base["sac_error"]
