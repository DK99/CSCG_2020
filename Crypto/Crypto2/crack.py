import math
from Crypto.Util.number import long_to_bytes

def getModInverse(a, m):
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def main():

    ct = 6213639477312598145146606285597413094756028916460209994926376562685721597532354994527411261035070313371565996179096901618661905020103824302567694878011247857685359643790779936360396061892681963343509949795893998949164356297380564973147847768251471545846793414196863838506235390508670540548621210855302903513284961283614161501466772253041178512706947379642827461605012461899803919210999488026352375214758873859352222530502137358426056819293786590877544792321648180554981415658300194184367096348141488594780860400420776664995973439686986538967952922269183014996803258574382869102287844486447643771783747439478831567060

    n = 0x57C88F1C9B9ED47D844F87B29F44796E17CE47C2FE24CC1AB7E34432B335212463D2399D074711800572EA6812E2901202BC5F190CCB4966D570904A41697A6364488AE140B1B6357FC6A6B4ACCD517A7403BBC996DFD072895F6A9A1EA8F2A6DAB69DA15575177F4CEF1ADB90825BBD4FEC5001AAC01A70E8A10E101334713932BE47D1A09D70D31157FE26E553774F8D9E502098472BCA8707931E2BC9CB92AAC94451BE6F1E558B93A8685CE984F4840AFAF8D2A8AD0D46545462A918151A50DEA1A28F4DF1E5E699B0052DA523059EB21D56B67C91E56AB75F35BC9F649BEA76A136B170D3A676F514B9C8955EAF78A90BADD5485BBA7F12178B1F8FEFEF
    e = 65537

    a = math.isqrt(n)
    b = a

    b2 = a * a - n

    while b*b != b2:
        a = a + 1
        b2 = a * a - n

        b = math.isqrt(b2)

    p = a + b
    q = a - b

    print("p: " + str(p))

    print("q: " + str(q))

    # Compute phi(n)
    phi = (p - 1) * (q - 1) 
    print("phi: " + str(phi))

    print("e: " + str(e))
    # Compute modular inverse of e
    d = getModInverse(e, phi)

    print("d: " + str(d))
    # Decrypt ciphertext
    pt = pow(ct, d, n)
    decrypted = str(pt)
    print("\n\npt: " + long_to_bytes(decrypted).decode("utf-8"))

if __name__ == "__main__":
    main()