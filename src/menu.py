import pygame

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse_x, mouse_y):
			if pygame.mouse.get_pressed()[0]:
				return True
		return False

	def changeColor(self, normal_button, selected_button):
		mouse_x, mouse_y = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse_x, mouse_y):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
			self.image = selected_button
		else:
			self.image = normal_button
			self.text = self.font.render(self.text_input, True, self.base_color)

class Titles:

	def __init__(self, pos_x, pos_y, text, color, font_size):

		font = pygame.font.Font("assets\\images\\Menu\\font.ttf", font_size)
		self.font = font
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.text = text
		self.color = color

	def draw(self, screen):
		text_surface = self.font.render(self.text, True, self.color)
		text_rect = text_surface.get_rect(center=(self.pos_x, self.pos_y))
		screen.blit(text_surface,text_rect)