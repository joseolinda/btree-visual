import pygame
import sys
import math

# Definindo a classe para um nó da árvore
class TreeNode:
    def _init_(self, value):
        self.value = value
        self.left = None
        self.right = None

# Função para criar uma árvore binária balanceada completa
def create_balanced_tree(values):
    if not values:
        return None
    
    mid = len(values) // 2
    root = TreeNode(values[mid])
    root.left = create_balanced_tree(values[:mid])
    root.right = create_balanced_tree(values[mid+1:])
    
    return root

# Função para exibir a árvore visualmente usando Pygame
def display_tree(screen, node, x, y, x_offset, level):
    if node:
        font = pygame.font.Font(None, 36)
        text = font.render(str(node.value), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)

        if node.left:
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x - x_offset // 2, y + 80), 2)
            display_tree(screen, node.left, x - x_offset // 2, y + 80, x_offset // 2, level + 1)

        if node.right:
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x + x_offset // 2, y + 80), 2)
            display_tree(screen, node.right, x + x_offset // 2, y + 80, x_offset // 2, level + 1)

# Configurações iniciais do Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Visualização de Árvore")
clock = pygame.time.Clock()

# Valores a serem inseridos na árvore
values_to_insert = []

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Inserir valores na lista
            elif pygame.K_1 <= event.key <= pygame.K_9:
                value = event.key - pygame.K_1 + 1
                values_to_insert.append(value)

    # Limpar a tela
    screen.fill((0, 0, 0))

    # Criar a árvore binária balanceada completa
    root = create_balanced_tree(values_to_insert)
    
    # Exibir a árvore
    if root:
        tree_height = int(math.log2(len(values_to_insert) + 1))
        display_tree(screen, root, 400, 100, 300, tree_height)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
