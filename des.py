import textwrap

# -------------------------------------------------------------------------keygeneration--------------------------------
global PC1,PC2
PC1= [56, 48, 40, 32, 24, 16,  8,
        0, 57, 49, 41, 33, 25, 17,
		9,  1, 58, 50, 42, 34, 26,
    	18, 10,  2, 59, 51, 43, 35,
		62, 54, 46, 38, 30, 22, 14,
		6, 61, 53, 45, 37, 29, 21,
		13,  5, 60, 52, 44, 36, 28,
		20, 12,  4, 27, 19, 11,  3
]

LSR=[1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]#shifts for each round

PC2=[13, 16, 10, 23,  0,  4,
	 2, 27, 14,  5, 20,  9,
	 22, 18, 11,  3, 25,  7,
	 15,  6, 26, 19, 12,  1,
	 40, 51, 30, 36, 46, 54,
	 29, 39, 50, 44, 32, 47,
	 43, 48, 38, 55, 33, 52,
	 45, 41, 49, 35, 28, 31
]




def roundkeys(bin1):

    k56=pe_2(PC1,bin1)#apply pc1
    LR28=textwrap.wrap(k56,28) #split 28 bit
    
    roundkeys=[]
    L=LR28[0]
    R=LR28[1]
    
    for i in LSR:
        L=L[i:]+L[:i]
        R=R[i:]+R[:i]
        K48=pe_2(PC2,L+R)
        roundkeys.append(K48)
    return roundkeys
        
        
        
# --------------------------------------------------------------------------keygeneration---------------------------------

global EP,IP,Sbox,FinalP,IP_inv

Sbox= [[
    # S1
    14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
     0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
     4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
    15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
],[
    # S2
    15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
     3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
     0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
    13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
],[
    # S3
    10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
    13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
    13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
     1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
],[
    # S4
     7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
    13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
    10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
     3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
],[
    # S5
     2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
    14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
     4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
    11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
],[
    # S6
    12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
    10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
     9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
     4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
],[
    # S7
     4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
    13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
     1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
     6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
],[
    # S8
    13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
     1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
     7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
     2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
]]


IP=[
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7
]


IP_inv=[
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
]

FinalP=[
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

EP=[
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

# --------------------------------------------------------------xor-----------------------------------------
def opxor(A):
    K=0
    l=len(A[0])
    for i in A:
        K^=int(i,2)
    
    Kbin=bin(K).replace("0b","").zfill(l)
    # print(Kbin)
    return Kbin

# ----------------------------------------------------------------xor----------------------------------------

# ------------------------------------------------------------------apply-P,EP----------
def pe_2(tab,bin1):
    bin2=''
    for i in tab:
      bin2+=bin1[i-1]
    return bin2
    bin2=''


# -----------------------------------------------------------------apply-P,EP-------------

#-------------------------------------------------------------------bit-exp,split-------------
def L0_R0_32(bin1): #32bitsplit
    L_R=[]
    L_R=textwrap.wrap(bin1,32)
    return L_R

def exp_32_48(bin1):  #expand_32_48
    R=''
    R=pe_2(EP,bin1)
    return R

def R_48_6(bin1): #split_48_6
    R_Sb=[]
    R_Sb=textwrap.wrap(bin1,6)
    return R_Sb


# --------------------------------------------------------------------bit-exp,split------------

# ---------------------------------------------------------apply-Sbox----------------------------------


def Sbox_sub(R_Sb):
    R_4b=''
    box=0
    for i in R_Sb:
        bin1=i
        # print("bin1:",bin1)
        row=int((bin1[0]+bin1[5]),2)
        col=int(bin1[1:5],2)
        index=16*row+col
        # R_4b.append(bin(S_box[box][index])[2:].zfill(4))
        R_4b+=(bin(Sbox[box][index])[2:].zfill(4))
        box+=1
    return R_4b


# -------------------------------------------------------------S-box----------------------------------------


# --------------------------------------------------------------Round-function-------------------------------
def roundfn(L,R,key_48):
    #R_expansion
    R_exp_48=exp_32_48(R)
    k=R
    
    #R_xor_key
    A=[R_exp_48,key_48]
    R_key_48=opxor(A)
    
    #R_key_split_6x8
    R_key_6=R_48_6(R_key_48)
    
    #R_key_sbox
    R_Sbox_32=Sbox_sub(R_key_6)

    #R_pe
    R_pe_32=pe_2(FinalP,R_Sbox_32)
    
    # R_L_xor
    B=[R_pe_32,L]
    R_L_48=opxor(B)

    
    R=R_L_48
    L=k
    return L,R
# --------------------------------------------------------------------Round-function---------------------------------------

def encrypt(bin1,key):
    bin2=''
    
    #IP
    IP_pe=pe_2(IP,bin1)

    
    #L_R_HALVES
    LR=L0_R0_32(IP_pe)
    L=LR[0]
    R=LR[1]

    #16xRounds
    kgn=roundkeys(key)
    
    print("Rounds-encryption")
    print("L:0",L,"  R:0",R,"   e")
    for i in range(16):
        L,R=roundfn(L,R,kgn[i])
        print("L",i+1,":",L,"  R",i+1,":",R,"   e")
    #final swap    
    L,R=R,L
    # print(L,R,"swap")
    bin2=L+R
    # final-P_inverse
    ct=pe_2(IP_inv,bin2)

    print("\nciphertext:",ct,len(ct))

    return ct
    


#test DES-1'st run


    
# ---------------------------------------------------------------------------decryption--------------------------------

def decrypt(bin1,key):

    RL=pe_2(IP,bin1)
    A=L0_R0_32(RL)
    
    #swapping
    L,R=A[1],A[0]
    
    #keys
    kgn=roundkeys(key)
    print("\nRounds-decryption")
    print("L16 :",L,"  R16 :",R,"   d")
    for i in range(16):
        j=15-i
        R,L=roundfn(R,L,kgn[j])
        print("L",j,":",L,"  R",j,":",R,"   d")
    bin2=L+R
    PT=pe_2(IP_inv,bin2)
    return PT




ct=encrypt('10'*32,'10'*32)

print("\ndecipher:",decrypt(ct,'10'*32))




