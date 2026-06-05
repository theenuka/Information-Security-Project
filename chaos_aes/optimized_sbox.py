from .aes_tables import S_BOX
from .affine import affine_equiv_sbox

# Deterministically selected by chaos-guided affine search.
# Affine equivalence preserves AES-level nonlinearity and differential uniformity.
A_ROWS = [239, 47, 166, 214, 144, 28, 13, 162]     #here we use affine equivalent construction to preserve s-box strength
B_ROWS = [179, 14, 184, 87, 64, 152, 173, 142]
IN_XOR = 19
OUT_XOR = 32


def make_optimized_sbox() -> list[int]:        
    sbox = affine_equiv_sbox(S_BOX, A_ROWS, B_ROWS, IN_XOR, OUT_XOR)
    if sorted(sbox) != list(range(256)):      #construct s-box
        raise ValueError("Optimized S-Box is not bijective")
    return sbox
