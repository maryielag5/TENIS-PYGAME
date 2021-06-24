import pygame
from pygame.locals import *
import os
import sys
if not pygame.font: print 'Warning, fonts disabled'
# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
class Bola(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("images/ball.png", True)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT / 2
		self.speed = [0.5,-0.5]

	def actualizar(self, time, pala_jug, pala_cpu, puntos):
		self.rect.centerx += self.speed[0] * time
		self.rect.centery += self.speed[1] * time
		if self.rect.left <= 0:
			puntos[1] += 1
		if self.rect.right >= WIDTH:
			puntos[0] += 1
		if self.rect.left <= 0 or self.rect.right >= WIDTH:
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time
		if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
			self.speed[1] = -self.speed[1]
			self.rect.centery += self.speed[1] * time
		if pygame.sprite.collide_rect(self, pala_jug):
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time
			puntos[2] += 1
		if pygame.sprite.collide_rect(self, pala_cpu):
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time
			puntos[3] += 1
		return puntos


class Pala(pygame.sprite.Sprite):
	def __init__(self, x):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("images/pala.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = HEIGHT / 2
		self.speed = 0.5

	def mover(self, time, keys):
		if self.rect.top >= 0:
			if keys[K_UP]:
				self.rect.centery -= self.speed * time
		if self.rect.bottom <= HEIGHT:
			if keys[K_DOWN]:
				self.rect.centery += self.speed * time

	def ia(self, time, ball):
		if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
			if self.rect.centery < ball.rect.centery:
				self.rect.centery += self.speed * time
			if self.rect.centery > ball.rect.centery:
				self.rect.centery -= self.speed * time

class Text (pygame.font.Font):
    def __init__ (self, FontName = None, FontSize = 17):
        pygame.font.init()
        self.font = pygame.font.Font('images/17-years-ago.ttf',17)
        self.size = FontSize
    def escribir (self, pantalla, text, color, posicion):
        text = text
        x,y = posicion
        for i in text.split("puntuacion"):
            pantalla.blit(self.font.render(i, 1, color), (x, y))
            y += self.size
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Funciones
def load_image(filename, transparent=False):
          try: image = pygame.image.load(filename)
          except pygame.error, message:
                  raise SystemExit, message
          image = image.convert()
          if transparent:
                  color = image.get_at((0,0))
                  image.set_colorkey(color, RLEACCEL)
          return image
  # ---------------------------------------------------------------------
  # ---------------------------------------------------------------------
def main(nombre):
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Tenis Pygame")
	RED = (200,0,0)
	white = (255,255,255)
	AZUL = (0, 0, 225)
	VERDE = (0, 0, 90)
	NEGRO = (0, 0, 0)
	i = 1
	text = Text()
	background_image = load_image('images/fondo.png')
	
	bola = Bola()
	pala_jug = Pala(12)
	pala_cpu = Pala(WIDTH - 12)
	clock = pygame.time.Clock()
	puntos = [0, 0, 0, 0]
	while True:
		time = clock.tick(60)
		keys = pygame.key.get_pressed()
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				favor1=str(puntos[2])
				text.escribir(screen, "PUNTOS TOTAL ACUMULADOS:"+favor1, white, (340, 200))
				text.escribir(screen, " LLEGO AL NIVEL: "+ str(i), RED, (340, 220))
				text.escribir(screen, " BYE, BYE, BYE BYE,ADIOS HASTA PRONTO ", NEGRO, (230, 350))
				text.escribir(screen, " ESPERE 5 SEGUNDOS MIENTRAS SE CIERRA.", VERDE, (230, 380))
				pygame.display.flip()
				clock.tick(0.2)
				sys.exit(0)
		puntos = bola.actualizar(time, pala_jug, pala_cpu, puntos)
		pala_jug.mover(time, keys)
		pala_cpu.ia(time, bola)
		screen.blit(background_image, (0, 0))
		text.escribir(screen,"JUGADOR:"+nombre, AZUL, (80, 40))
		contra1=str(puntos[1])
		text.escribir(screen, "P.CONTRA:"+contra1, white, (20, 10))
		favor1=str(puntos[2])
		text.escribir(screen, "P.FAVOR:"+favor1, white, (200, 10))
		contra2=str(puntos[0])
		text.escribir(screen, "P.CONTRA: "+contra2, RED, (500, 10))
		favor2=str(puntos[3])
		text.escribir(screen, "P.FAVOR:"+ favor2, RED, (330, 10))
		screen.blit(bola.image, bola.rect)
		screen.blit(pala_jug.image, pala_jug.rect)
		screen.blit(pala_cpu.image, pala_cpu.rect)
		v= 4 * i
		if puntos[2]== v :
			i += 1
			text.escribir(screen, " NIVEL: "+ str(i), RED, (310, 220))
			pygame.display.flip()
			clock.tick(0.4)
		pygame.display.flip()
		
	return 0
if __name__ == '__main__':
    print "INGRESE NOMBRE PARA EMPEZAR JUEGO"
    n = raw_input()
    main(n)
