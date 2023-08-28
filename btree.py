import pygame # pip install pygame
import sys
import math
import pygame_gui # pip install pygame_gui

# Definindo a classe para um nó da árvore
class TreeNode:
    def __init__(self, value):
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

# Função para criar uma árvore binária de busca
def create_binary_search_tree(values):
    root = None
    for value in values:
        root = insert_into_bst(root, value)
    return root

# Função para inserir um valor em uma árvore binária de busca
def insert_into_bst(root, value):
    if root is None:
        return TreeNode(value)
    
    if value < root.value:
        root.left = insert_into_bst(root.left, value)
    else:
        root.right = insert_into_bst(root.right, value)
    
    return root

# Função para exibir a árvore visualmente usando Pygame
def display_tree(screen, node, x, y, x_offset, y_spacing, level=1):
    if node:
        font_size = 30  # Tamanho da fonte
        font = pygame.font.Font(None, font_size)
        
        node_radius = 15
        y_spacing = 80 + level * 10  # Ajuste o espaçamento com base no nível

        pygame.draw.circle(screen, (255, 255, 255), (x, y), node_radius)

        text = font.render(str(node.value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

        if node.left:
            pygame.draw.line(screen, (255, 0, 0), (x, y), (x - x_offset, y + y_spacing), 2)
            display_tree(screen, node.left, x - x_offset, y + y_spacing, x_offset // 2, y_spacing, level + 1)

        if node.right:
            pygame.draw.line(screen, (0, 0, 255), (x, y), (x + x_offset, y + y_spacing), 2)
            display_tree(screen, node.right, x + x_offset, y + y_spacing, x_offset // 2, y_spacing, level + 1)

# Configurações iniciais do Pygame
pygame.init()
WINDOW_SIZE = (1024, 720)
BACKGROUND_COLOR = (120, 120, 120)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Visualização de Árvore")
clock = pygame.time.Clock()

# Valores a serem inseridos na árvore
values_to_insert = []

# Inicialização do pygame_gui
manager = pygame_gui.UIManager(WINDOW_SIZE)

# Botões de rádio para escolher o tipo de árvore
radio_button_rect = pygame.Rect(10, 10, 100, 20)
radio_button_bst = pygame_gui.elements.UIButton(relative_rect=radio_button_rect, text='BST', manager=manager)
radio_button_rect.move_ip(110, 0)
radio_button_balanced = pygame_gui.elements.UIButton(relative_rect=radio_button_rect, text='Balanceada', manager=manager)
selected_tree = 'BST'  # Árvore binária de busca por padrão

# Campo de entrada para valores
input_rect = pygame.Rect(10, 40, 150, 20)
input_field = pygame_gui.elements.UITextEntryLine(relative_rect=input_rect, manager=manager)

# Botão "Adicionar"
add_button_rect = pygame.Rect(170, 40, 80, 20)
add_button = pygame_gui.elements.UIButton(relative_rect=add_button_rect, text='Adicionar', manager=manager)

# Loop principal
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == radio_button_bst:
                    selected_tree = 'BST'
                elif event.ui_element == radio_button_balanced:
                    selected_tree = 'Balanceada'
                elif event.ui_element == add_button:
                    try:
                        value = int(input_field.get_text())
                        values_to_insert.append(value)
                        input_field.set_text('')  # Limpar o campo de entrada
                    except ValueError:
                        pass  # Ignorar entrada inválida

        manager.process_events(event)

    # Atualizar a interface gráfica
    manager.update(time_delta)

    # Limpar a tela
    screen.fill(BACKGROUND_COLOR)

    # Criar a árvore selecionada
    if selected_tree == 'Balanceada':
        root = create_balanced_tree(values_to_insert)
    elif selected_tree == 'BST':
        root = create_binary_search_tree(values_to_insert)
    
    # Exibir a árvore
    if root:
        tree_height = int(math.log2(len(values_to_insert) + 1))
        display_tree(screen, root, 512, 50, 250, 40, tree_height)

    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
