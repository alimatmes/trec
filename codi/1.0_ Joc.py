import pygame
from pytmx.util_pygame import load_pygame


def pintar_mapa (finestra, dadesmapa, desplacament):
    for capa in dadesmapa: #el priemr bucle opte totes les capes del dibux/mapa, que en aqeust cas es només una
        for bloc in capa.tiles(): #per cada capa que opte el bucle agafa cada patró de la capa que està en aquest moment
            x_pos= bloc[0] * 32 + desplacament[0] #per cada patro obtenim la cordenada x i y  i el dibuix (si o si ha de ser el úmero 0 la x, el número 1 la y i el numero 2 la imatge del patró)
            y_pos=bloc[1] * 32 + desplacament[1] - bloc[2].get_rect().height # se li resta l'altura del personatge degut a que estaria a sota d'on volem ja que quan posa la cordenada agafa la foto a la prat d'adalt de lesquerra i es resta per a que estigui més adalt
            
            finestra.blit(bloc[2], (x_pos, y_pos))
            
def obte_propietats_blocs(dadesmapa,x,y,desplacament):
    mon_x= x - desplacament[0] #el desplacament serveix per a moure el mapa
    mon_y= y - desplacament[1]
    
    bloc_x = mon_x // 32 #això es per a saber en quin bloc estem
    bloc_y = mon_y // 32
    
    propietats=""
    # print("Entro"+str(x)+" - " + str(y))
    propietats= dadesmapa.get_tile_properties(bloc_x, bloc_y, 0)#el número 0 es per a la capa, està en la capa 0 
    
    if propietats == None:#si no hi ha ningun patró a sota que totes les variables que livaig posar als patrons siguin falsa per a dsp programar que caigui
        propietats = {"escales": False, "terra": False, 'salut':0,
                      'punts':0, 'solid':False, 'dona': '', 'requereix': ''}
        
    return propietats


ANCHO=800
ALTO=600
VELOCITAT = 4 #

mon_desplacament = [0,0]

#---Colores

NEGRO=(0,0,0)
BLANCO=(255,255,255)
ROJO=(255,0,0)
VERDE=(0,255,0)
AZUL=(0,0,255)

#---iniciar pygame
pygame.init()

#---Crear ventana
ventana=pygame.display.set_mode((ANCHO,ALTO))

    #Fons
fons_introduccio=pygame.image.load('fotos/paper.jpg')
#ventana.blit(fons_introduccio, (0,0))
ventana.fill ('White')

#--- Carrega mapa
dades_mapa=load_pygame("mapa/prova_mapa.tmx")

#--- Mida mapa
mapa_ample= dades_mapa.width * dades_mapa.tilewidth
#print (mapa_ample)

#---Definir una fuente de texto
fuente_introduccio_1=pygame.font.Font("text/hola.ttf", 100)
fuente_introduccio_2=pygame.font.Font("text/hola.ttf", 50)

#---Text
introduccio_1= fuente_introduccio_1.render('Benvingut', 1, '#664e1b') 
ventana.blit (introduccio_1, (160,90))

introduccio_2=fuente_introduccio_2.render('Per a començar apreta SPACE', 1, 'Black')
ventana.blit (introduccio_2, (50, 350))
introduccio_3=fuente_introduccio_2.render('Per a sortir apreta ESC', 1, 'Black')
#ventana.blit(introduccio_3, (101,425))

#--- Zona dibuix primer nivell
        #Introducció

terra_1=pygame.Surface((800,150)) #Això s'ha de canviar per a imatges
terra_1.fill('Green')

personatge=pygame.Surface((40,65))
personatge_rect = personatge.get_rect()
personatge.fill('Red')

        # 1r nivell

direccio='quiet_dreta' #això és per a que des d'un principi, el personatge que suti sense tocar res sigui aquest i axi no hi hagui error


personatge_quiet_dreta = pygame.image.load('personatges/personatge_quiet/tile005.png').convert_alpha()

personatge_quiet_esquerra = pygame.image.load('personatges/personatge_quiet/personatge_quiet_esquerra.png').convert_alpha()
 
personatge_salt_abaix_dreta= pygame.image.load('personatges/personatge_salt/tile000.png ').convert_alpha()

personatge_salt_amunt_dreta=pygame.image.load('personatges/personatge_salt/tile002.png').convert_alpha()

personatge_salt_abaix_esquerra=pygame.image.load('personatges/personatge_salt/personatge_salt_esquerra.png').convert_alpha()

personatge_salt_amunt_esquerra=pygame.image.load('personatges/personatge_salt/personatge_salt_amunt_esquerra.png').convert_alpha()


personatge_dret = [ #aqui cargem todes les imaagtes per a després que personatge_dret_contador vagui anant d'una en una per fer un sprite
pygame.image.load('personatges/personatge_2/tile000.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile001.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile002.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile003.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile004.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile005.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile006.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile007.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile008.png').convert_alpha(),
pygame.image.load('personatges/personatge_2/tile009.png').convert_alpha()
    
]
personatge_esquerra = [

    pygame.transform.flip(image,True,False) for image in personatge_dret
#aquest codi serveix per a invertir la imatge, fa que en cada imatge de personatge_dret la vagui girant (transform.flip)
#el true serveix per a girar la x 
#el false es per a girar la y (que en aquest cas no vull que estigui del revés)
    
]

mida_personatge =personatge_quiet_dreta.get_rect()


    #---ENEMIC
foc_enemic= [
pygame.image.load('personatges/foc_enemic/tile000.png').convert_alpha(),
pygame.image.load('personatges/foc_enemic/tile001.png').convert_alpha(),
pygame.image.load('personatges/foc_enemic/tile002.png').convert_alpha(),
pygame.image.load('personatges/foc_enemic/tile003.png').convert_alpha(),
pygame.image.load('personatges/foc_enemic/tile004.png').convert_alpha(),
pygame.image.load('personatges/foc_enemic/tile005.png').convert_alpha(),
pygame.image.load('personatges/foc_enemic/tile006.png').convert_alpha(),
]


  
estructura_1=pygame.Surface((200, 70)) #el cel que s'ha de canviar 
estructura_1.fill('Blue')

#---Crear reloj
reloj=pygame.time.Clock()

#---Título
pygame.display.set_caption("1.0_ JOC")

#---Zona de variables del programa
imatge='hola'

#---Posició
y_inicial = 100
x_pers=80
y_pers=y_inicial 

#-- Velocitat 
y_vel = 0
x_vel=0


#---Contador
personatge_dreta_contador_sprite=0
personatge_esquerra_contador_sprite=0
personatge_salt_altura=0
foc_enemic_contador_sprite=0




# -- gravity 
gravity = 1


#---Bucle principal

jugar=True
menu = True

while jugar:
    
    a_sobre= obte_propietats_blocs(dades_mapa,
                                   x_pers + mida_personatge.width // 2,
                                   y_pers + mida_personatge.height + 32,
                                   mon_desplacament)
    
    for event in pygame.event.get():
        
        
        if event.type==pygame.QUIT:
            jugar=False
        
        #---Eventos teclado
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: #Si s'apreta Esc el joc s'apaga 
                jugar=False
                
            if event.key==pygame.K_SPACE: #Si s'apreta Space el joc pasa a un altre pagina
                if (menu== True ):
                    ventana.fill('Blue')
                    menu=False #aquí fem que aquesta funcio del space s'elimini i ja quan inicies sessió l'nicautitltiat serà per a que salti el personatge
        


            if event.key==pygame.K_UP:
                if direccio=='esquerra' or direccio=='quiet_esquerra':
                    imatge='esquerra_salt'
                    #print("esquerra salt")
                    
                if direccio=='dreta' or direccio=='quiet_dreta':
                    imatge='dreta_salt'
                    print("dreta salt")

                    
                if a_sobre['terra']==True:
                    personatge_salt_altura=40
            
            if event.key==pygame.K_LEFT: # això es el moviment cap a l'esquerra
                direccio='esquerra'
                x_vel = -VELOCITAT
            if event.key==pygame.K_RIGHT: #aquest es el moviment cap a la dreta
                direccio='dreta'
                x_vel = VELOCITAT
            
            
        if event.type==pygame.KEYUP: #aquí indiquem amb el keyup que quan la tecla no està presionada la velocitat es nula i la imatge del personatge a de ser la de quiet
            if event.key==pygame.K_LEFT:
                x_vel=0
                direccio="quiet_esquerra"
            if event.key==pygame.K_RIGHT:
                x_vel=0
                direccio="quiet_dreta"
    
    #print(a_sobre)
    if personatge_salt_altura>0: #aqui es fa la variable de salt, metre que l'altura sigui major a trenta el prsonatge salti
        if imatge=='esquerra_salt':
            direccio='salt_amunt_esquerra'
            print ("esquerra")
        else: 
            direccio='salt_amunt_dreta'
        y_vel=-2
        personatge_salt_altura -= 1
    elif a_sobre['terra'] ==False: #ja quan aquell bucle s'acaba ve a aquest per a baixar
        if imatge=='esquerra_salt':
            direccio='salt_abaix_esquerra'
            print ('salt_abaix_esquerra')
        else: 
            direccio='salt_abaix_dreta'
            print('salt_abaix_dreta')
        y_vel=3
    else: #ja quan no compleix cap de les dues ve a aquí per a ja quedar-se quiet
        y_vel = 0
        
          
    a_dreta= obte_propietats_blocs(dades_mapa,
                                   x_pers + mida_personatge.width-50, #Es resta el cincuanta per ajustar la foto, que te un espai vuit davant // la mida es per a saber des de el punt dreta
                                   y_pers + mida_personatge.height // 2 + 85,
                                   mon_desplacament) 
    
    a_esquerra =obte_propietats_blocs (dades_mapa,
                                       x_pers + 50,
                                       y_pers + mida_personatge.height //2 + 85,
                                       mon_desplacament)
    a_dalt = obte_propietats_blocs(dades_mapa,
                                   x_pers + mida_personatge.width//2,
                                   y_pers +85,
                                   mon_desplacament)




    if a_dreta['solid'] ==True and (direccio=="dreta" or direccio=="personatge_salt_amunt_dreta" or direccio=="personatge_salt_abaix_dreta"):
        x_pers-=x_vel
    
    if a_esquerra ['solid'] ==True and direccio=="esquerra":
        print ("holiiss")
        x_pers-=x_vel
    
    if a_dalt ['solid'] == True and (direccio=='salt_amunt_esquerra'or direccio=='salt_amunt_dreta'):
        personatge_salt_altura=0 #Es posa a 0 ja que abans vaig rpogramar que si es menor que 0 el personatge ja havia de baizar (233-239)
    
    x_pers+=x_vel
    y_pers+=y_vel
    #print (x_pers)
    #print (mon_desplacament[0])

    if x_pers > ventana.get_width()/2 and (mon_desplacament[0]*-1) < (mapa_ample-ANCHO): #Si el personatge arriba a la meitat de la pantalla
        x_pers =ventana.get_width()/2 #Es queda quiet

        mon_desplacament[0] -= VELOCITAT #

    if x_pers < ventana.get_width()/2 and mon_desplacament[0] < 0:
        x_pers=ventana.get_width()/2

        mon_desplacament[0] += VELOCITAT




    if menu == False:
        ventana.fill('Black') #la part que no he posat ningún ptaró que estigui de color negre
        pintar_mapa(ventana, dades_mapa, mon_desplacament)#aquí posem el mapa 

        
        
        if direccio=='dreta':
            personatge_dreta_contador_sprite = (personatge_dreta_contador_sprite + 1 ) % len(personatge_dret) 
            ventana.blit(personatge_dret[personatge_dreta_contador_sprite], (x_pers,y_pers))
            # 10 --> len(personatge_dreta) 
            # l len es per a treure el residu i quan es a la foto 1, es suma +1, 
            # i es diviideix entre el nombre de participants que hia ha en personatge_dret fent que el residu 
            # sigui dos i la foto que surti en aquell moment sigui la dos
            
            # if personatge_dreta_index==9:
            #     personatge_dreta_index=0
            # else: 
            #     personatge_dreta_index +=1
            
        if direccio=='esquerra':
            ventana.blit(personatge_esquerra[personatge_esquerra_contador_sprite], (x_pers,y_pers))   
            if personatge_esquerra_contador_sprite==9:
                personatge_esquerra_contador_sprite=0
            else:
                personatge_esquerra_contador_sprite+=1 
        
        if direccio == 'quiet_dreta':
            ventana.blit(personatge_quiet_dreta,(x_pers,y_pers))
        
        if direccio == 'quiet_esquerra':
            ventana.blit(personatge_quiet_esquerra,(x_pers, y_pers))

        if direccio == 'salt_abaix_dreta':
            ventana.blit(personatge_salt_abaix_dreta, (x_pers, y_pers))
            
        if direccio== 'salt_amunt_dreta':
            ventana.blit(personatge_salt_amunt_dreta, (x_pers,y_pers))
        
        if direccio=='salt_abaix_esquerra':
            ventana.blit(personatge_salt_abaix_esquerra,(x_pers,y_pers))
        
        if direccio =='salt_amunt_esquerra':
            ventana.blit(personatge_salt_amunt_esquerra,(x_pers,y_pers))
        
        if foc_enemic_contador_sprite==7: #acabar de fer-ho
            foc_enemic_contador_sprite=0
        else:
            foc_enemic_contador_sprite+=1


    
    pygame.display.flip()
    pygame.time.delay(5)


    reloj.tick(60)






    pygame.display.flip()

pygame.quit()