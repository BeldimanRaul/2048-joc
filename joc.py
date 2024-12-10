import pygame
import random
import math

pygame.init()
#INITIALIZAM VARIABILE PT FEREASTRA JOCULUI ,SI ALTELE
FPS=60

WIDTH,HEIGHT=800,800
RANDURI=4
COLOANE=4
INALTIME_PAT=HEIGHT//RANDURI
LUNGIME_PAT=WIDTH//COLOANE
CULOARE_MARGINI=(184,176,160)
GROSIME=10
FUNDAL=(205,192,180)
CULOARE_FONT=(119,110,101)


INTERFATA=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("joc 2048")
FONT=pygame.font.SysFont("sans",60,bold=True)
MISCARE=20


class Patrat:
     CULORI = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]
     
     def __init__(self,valoare,rand , coloana):
         self.valoare=valoare
         self.rand=rand
         self.coloana=coloana
         self.x=coloana*LUNGIME_PAT
         self.y=rand*INALTIME_PAT


     def get_culoare(self,interfata) :
         index_culoare=int(math.log2(self.valoare))-1
         culoare=self.CULORI[index_culoare]
         return culoare
     


     def desen(self,interfata):
         culoare=self.get_culoare(interfata)
         pygame.draw.rect(interfata,culoare,(self.x,self.y,LUNGIME_PAT,INALTIME_PAT))
         text=FONT.render(str(self.valoare),1,CULOARE_FONT)
         interfata.blit(
             text,
             (self.x+(LUNGIME_PAT/2-text.get_width()/2),
             self.y+(INALTIME_PAT/2-text.get_height()/2),
             
             ),
         )

     

     def miscari(self,delta) :
         self.x += delta [0]
         self.y+= delta[1]


     def seteaza_pozitie():
         pass   

def desen_p(interfata):
    for rand in range(1,RANDURI):
        y=rand*INALTIME_PAT
        pygame.draw.line(interfata,CULOARE_MARGINI,(0,y),(WIDTH,y),GROSIME)
        
    for coloana in range(1,COLOANE):
        x=coloana*LUNGIME_PAT
        pygame.draw.line(interfata,CULOARE_MARGINI,(x,0),(x,HEIGHT),GROSIME)


    pygame.draw.rect(interfata,CULOARE_MARGINI,(0,0,WIDTH,HEIGHT),GROSIME)
 

def desen(interfata,patrate):
    interfata.fill(FUNDAL)
    
    for patrat in patrate.values():
        patrat.desen(interfata)   
   
    desen_p(interfata)
    pygame.display.update()


def get_pozitie_random(patrate):
    rand=None
    coloana=None
    while True:
        rand=random.randrange(0,RANDURI)
        coloana=random.randrange(0,COLOANE)
        if f"{rand}{coloana}" not in patrate:
            break
    return rand,coloana


def muta_patrate(interfata,patrate,ceas,directie):
    updated=True
    blocuri=set()

    if directie =="stanga":
        functie_sortare=lambda x: x.coloana
        revers=False
        delta=(-MISCARE,0)
        boundary_check=lambda patrat: patrat.coloana==0
        get_urmatoarea=lambda patrat: patrate.get(f"{patrat.rand}{patrat.coloana-1}")
        merge_check=lambda patrat, urmatoru_patrat: patrat.x>urmatoru_patrat.x+MISCARE
        move_check=lambda patrat , urmatoru_patrat: patrat.x > urmatoru_patrat.x+LUNGIME_PAT+MISCARE
        tavan=True
    elif directie=="dreapta":
        pass
    elif directie=="sus":
        pass
    elif directie=="jos":
        pass

    while updated:
        ceas.tick(FPS)
        updated=False
        patrate_sortate=sorted(patrate.vaues(),key=functie_sortare,reverse=revers)

        for i ,patrat in enumerate(patrate_sortate):
            if boundary_check(patrat):
                continue
            urmatorul_patrat=get_urmatoarea(patrat)
            if not urmatorul_patrat:
                patrat.miscari(delta)
            elif (patrat.valoare==urmatorul_patrat.valoare and patrat not in blocuri and urmatorul_patrat not in blocuri):
                if merge_check(patrat,urmatorul_patrat):
                    patrat.miscari(delta)
                else:
                    urmatorul_patrat.valoare*=2 
                    patrate_sortate.pop(i) 
                    blocuri.add(urmatorul_patrat)
            elif move_check(patrat, urmatorul_patrat):
                patrat.miscari(delta)
            else:
                continue   

            updated=True 


def genereaza_patrate():
    patrate={}
    for _ in range(2):
        rand,coloana=get_pozitie_random(patrate)
        patrate[f"{rand}{coloana}"]=Patrat(2,rand,coloana)

    return patrate



def main(interfata):
    ceas=pygame.time.Clock()
    run=True

    patrate = genereaza_patrate()

    while run:
        ceas.tick(FPS)

        for eveniment in pygame.event.get():
            if eveniment.type==pygame.QUIT:
                run=False  
                break
        desen(interfata,patrate)   
    pygame.quit()        

if __name__=="__main__":
    main(INTERFATA)
