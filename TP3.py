import gensafeprime
import random
import time

#générer deux chiffres aléatoires premiers  p et q
p = gensafeprime.generate(1024);
q = gensafeprime.generate(1024);

print('Affichage de la valeur de p : ',p)
print('Affichage de la valeur de q : ',q)


N = p*q;
print('Affichage de la valeur de N :', N);

#Fi est le 𝜑(𝑁)  vu en cours 
Fi= (p-1)*(q-1);
print ('Affichage de la valeur de Fi :', Fi);

# e est l'une des valeurs de la clé public , elle a été énnoncée dans le TP
e= 65537;
print("Affichage de la valeur de e :",e)



# pour effectuer l'inversion modulaire on implémente deux fonctions qui sont extended_gcd et inverse_modulaire 
def extended_gcd(val1, val2):
    lastremainder, remainder = abs(val1), abs(val2)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if val1 < 0 else 1), lasty * (-1 if val2 < 0 else 1)
 
def inverse_modulaire(val1, val2):
    g, x, y = extended_gcd(val1, val2)
    #if g != 1:
       # raise ValueError
    return x % val2


# d est l'inverse de e modulo Fi , (N, d ) est notre clé privé
d = inverse_modulaire(e, Fi)
print('Affichage de la valeur de d :', d)


print(' Affichage de la  clé public : ', e, N);
print(' Affichage de la  clé privée : ', d, N);


# génération d'un message aléatoire d'une longueur max de 2048 bits 
message_1= random.getrandbits(2048);
print(' Affichage du message :', message_1)

# modexp est notre fonction d'exponanciation rapide modexp(b, e, m)= 𝑏^𝑒 mod 𝑚
def modexp(x, y, z):
    "Calculate (x ** y) % z efficiently."
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number


message_1_chiffre =(modexp(message_1,e, N))
print("Affichage du message chiffré ", message_1_chiffre)


message_1_dechiffre =(modexp(message_1_chiffre,d,N))
print("Affichage du message déchiffré", message_1_dechiffre)


signature_message_1= (modexp(message_1,d,N))
print("Affichage de la signature du message ", signature_message_1)


message_signature= (modexp(signature_message_1, e, N))
print("Vérification de la signature ",message_signature)

#fonction qui calcule le temps d'exection du code pour faire le calcul de 100 fois la signature 
def calcul_time ():
    t= round(time.time()*1000)
    for x in range(0,100):
        me=random.getrandbits(90)
        signature= (modexp(me,d,N))
    t1=round(time.time()*1000)
    print(t1)
    print(t)
    t2=t1-t
    print("Le temps d'execution de 100 fois la signature est :", t2)
    return t2
calcul_time()



dp = d %(p-1)
print('Affichage de la valeur de dp :', dp)

dq = d %(q-1)
print("Affichage de la valeur de  dq :", dq)

iq=inverse_modulaire(q,p)
print("Affichage de la valeur de qi : ", iq)

sp = modexp(message_1,dp,p)
print("Affichage de la valeur de sp :",sp)

sq = modexp(message_1,dq,q)
print("Affichage de la valeur de sq :",sq)

scrt=sq+q*(iq*(sp-sq)%p)
print("Affichage de la nouvelle valeur de la signature  scrt : ",scrt)

message_scrt= (modexp(scrt,e,N))
print('Verification de la  signature scrt :', )


#fonction qui calcule le temps d'execution du code pour faire le calcul de 100 fois la nouvelle signature scrt
def calcul_time_2 ():
    t= round(time.time()*1000)
    for x in range(0,100):
        me=random.getrandbits(90)
        sp = modexp(me,dp,p)
        sq = modexp(me,dq,q)
        signature= sq+q*(iq*(sp-sq)%p)
    t1=round(time.time()*1000)
    print(t1)
    print(t)
    t2=t1-t
    print('le temps d exection de 100 fois la nouvell signature ',t2)
    return t2

calcul_time_2()

#valeur de la signature avant l'injection de fautes
bellecore_s =0x3f010be37eb5eca9

#valeur de la signature après l'injection de fautes
bellecode_s_faute = 0x014cad4a340f946ad9

#fonction qui caclule le pgcd de deux nombres 
def pgcd(a,b):
    """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b"""
    if b==0:
        return a
    else:
        r=a%b
        return pgcd(b,r)

#le nouveau N de la nouvelle clé
new_N = 47775493107113604137 ;
print("Affichage de la nouvelle valeur de  N :", new_N)

#le nouveau e de la nouvelle clé
new_e = 17;
print("Affichage de la nouvelle valeur de e ", new_e )


soustraction_bellecore_s =  abs (bellecore_s - bellecode_s_faute)
print("Affichage de la valeur de la soustraction avec la valeur absolue", soustraction_bellecore_s)

#on suppose une valeur de q et on calcule la valeur de p 
new_q =  pgcd(new_N, soustraction_bellecore_s)
print("Affichage de la nouvelle valeur q :", new_q )

new_p = new_N // new_q
print("Affichage de la nouvelle valeur p :", new_p)

new_s = (new_q - 1) * (new_p - 1)
print("Affichage de la nouvelle valeur s :", new_s)

new_d = inverse_modulaire(new_e, new_s)
print("Affichage de la nouvelle valeur d :",new_d)

#génération d'un nouveau message aléatoire 
new_message =random.getrandbits(32)
print('Affichage du message avant chiffrement :', new_message)

new_chiffr =(modexp(new_message,new_e,new_N))
print("Affichage du message après chiffrement :",new_chiffr)

new_dechiffr =(modexp(new_chiffr,new_d,new_N))
print("Affichage du message après déchiffrement : ", new_dechiffr)