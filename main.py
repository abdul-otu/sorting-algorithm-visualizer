import math
import random
import pygame
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	BLUE = 0, 0, 255
	RED = 255, 0, 0

	FONT = pygame.font.SysFont('Constantia', 20)
	SIDE_PADDING = 0
	TOP_PADDING = 125


	def __init__(self, width, height, elements):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_elements(elements)


	def set_elements(self, elements):
		self.elements = elements
		self.min_value = min(elements)
		self.max_value = max(elements)

		self.surface_width = round((self.width) / len(elements))
		self.surface_height = math.floor((self.height - self.TOP_PADDING) / (self.max_value - self.min_value))
		self.start_x = self.SIDE_PADDING



def insertion_sort(draw_info):
	elements = draw_info.elements

	for i in range(1, len(elements)):
		current = elements[i]

		while True:
			if not (i > 0 and elements[i - 1] > current):
				break

			elements[i] = elements[i - 1]
			i = i - 1
			elements[i] = current
			draw_elements(draw_info, {i - 1: draw_info.BLUE, i: draw_info.RED}, True)
			yield True
	return elements



def selection_sort(draw_info):
	elements = draw_info.elements
	
	for i in range(len(elements)-1):
		min=1
		
		for j in range(i+1, len(elements)-1):
			if elements[j] < elements[min]:
				min = j

		draw_elements(draw_info, {j: draw_info.BLUE, j + 1: draw_info.RED}, True)
		elements[i], elements[min] = elements[min], elements[i]
		yield True
	return elements



def bubble_sort(draw_info):
	elements = draw_info.elements

	for i in range(len(elements) - 1):
		for j in range(len(elements) - 1 - i):
			num1 = elements[j]
			num2 = elements[j + 1]

			if (num1 > num2):
				elements[j], elements[j + 1] = elements[j + 1], elements[j]
				draw_elements(draw_info, {j: draw_info.BLUE, j + 1: draw_info.RED}, True)
				yield True

	return elements



def draw(draw_info, algo_name):
	draw_info.window.fill(draw_info.WHITE)

	title = draw_info.FONT.render("Active: " + f"{algo_name}", 1, draw_info.BLUE)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R to Reset | ENTER to Start", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | S - Selection Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_elements(draw_info)
	pygame.display.update()



def draw_elements(draw_info, color_positions={}, clear_bg=False):
	elements = draw_info.elements

	if clear_bg:
		clear_rect = (draw_info.SIDE_PADDING, draw_info.TOP_PADDING, draw_info.width, draw_info.height - draw_info.TOP_PADDING)
		pygame.draw.rect(draw_info.window, draw_info.WHITE, clear_rect)

	for i, value in enumerate(elements):
		x = draw_info.start_x + i * draw_info.surface_width
		y = draw_info.height - (value - draw_info.min_value) * draw_info.surface_height

		color = draw_info.BLACK

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.surface_width, draw_info.height))

	if clear_bg:
		pygame.display.update()



def generate_starting_list(n, min_value, max_value):
	elements = []

	for _ in range(n):
		value = random.randint(min_value, max_value)
		elements.append(value)

	return elements



def main():
	run = True
	clock = pygame.time.Clock()

	n = 200
	min_value = 5
	max_value = 100

	elements = generate_starting_list(n, min_value, max_value)
	draw_info = DrawInformation(1000, 700, elements)
	sorting = False

	sorting_algorithm = insertion_sort
	sorting_algo_name = "Insertion Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(100)

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue
			if event.key == pygame.K_r:
				elements = generate_starting_list(n, min_value, max_value)
				draw_info.set_elements(elements)
				sorting = False
			elif event.key == pygame.K_RETURN and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info)
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"

	pygame.quit()



if __name__ == "__main__":
	main()