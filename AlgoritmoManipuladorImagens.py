from PIL import Image
import matplotlib.pyplot as plt

def calcular_media_rgb(caminho_pgm_entrada):
    # Carregar a imagem no formato PPM (P3)
    imagem = Image.open(caminho_pgm_entrada)
    imagem = imagem.convert("RGB")  # Garantir que esteja no modo RGB
    
    largura, altura = imagem.size
    pixels_p2 = []  # Para escala de cinza (P2)

    # Processar cada pixel para calcular a média de cinza (linha por linha)
    for y in range(altura):
        linha_p2 = []
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            media = (r + g + b) // 3  # Cálculo da média RGB
            linha_p2.append(media)
        pixels_p2.append(linha_p2)

    return pixels_p2, largura, altura

def plotar_graficos(pixels_p2, largura, altura):
    # Escolher uma linha específica para plotar
    linha_especifica = 10  # Por exemplo, a 10ª linha (ajuste conforme necessário)
    if linha_especifica < altura:
        plt.figure(figsize=(10, 5))
        plt.plot(range(largura), pixels_p2[linha_especifica], label=f"Linha {linha_especifica}", color='blue')
        plt.title(f"Valores de Cinza na Linha {linha_especifica}")
        plt.xlabel("Índice de Pixel (X)")
        plt.ylabel("Média Cinza (0-255)")
        plt.grid(True)
        plt.legend()
        plt.show()

    # Criar um histograma para a distribuição de tons de cinza na imagem inteira
    todos_valores = [valor for linha in pixels_p2 for valor in linha]
    plt.figure(figsize=(10, 5))
    plt.hist(todos_valores, bins=20, color='gray', edgecolor='black')
    plt.title("Distribuição de Tons de Cinza")
    plt.xlabel("Tons de Cinza (0-255)")
    plt.ylabel("Frequência")
    plt.grid(True)
    plt.show()

def converter_pgm_para_pbm_binario(input_path, output_path, limiar=128):
    # Carregar a imagem PGM (escala de cinza)
    imagem = Image.open(input_path)
    imagem = imagem.convert("L")  # Garantir que esteja em escala de cinza

    # Binarização com o limiar (PBM em ASCII - P1)
    imagem_binarizada = imagem.point(lambda p: 1 if p > limiar else 0)
    
    # Salvar como PBM ASCII (P1)
    with open(output_path, 'w') as f:
        f.write("P1\n")
        f.write(f"{imagem.width} {imagem.height}\n")
        for y in range(imagem.height):
            linha = "".join(str(imagem_binarizada.getpixel((x, y))) + " " for x in range(imagem.width))
            f.write(linha.strip() + "\n")
    print(f"Arquivo PBM binário salvo em {output_path}")

def aplicar_negativo(input_path, output_path):
    # Carregar a imagem binarizada (escala de cinza)
    imagem = Image.open(input_path)
    imagem = imagem.convert("L")  # Garantir que esteja em escala de cinza

    # Aplicar o negativo
    imagem_negativa = imagem.point(lambda p: 255 - p)
 
    # Salvar a imagem no formato PGM ASCII (P2)
    with open(output_path, 'w') as f:
        f.write("P2\n")
        f.write(f"{imagem.width} {imagem.height}\n255\n")
        for y in range(imagem.height):
            linha = " ".join(str(imagem_negativa.getpixel((x, y))) for x in range(imagem.width))
            f.write(linha + "\n")
    print(f"Imagem negativa PGM salva em {output_path}")

def gerar_histograma_rgb(caminho_pgm_entrada):
    """
    Gera histogramas separados para os canais de cor (Red, Green, Blue) de uma imagem RGB.

    :param caminho_pgm_entrada: Caminho para a imagem de entrada no formato RGB.
    """
    # Carregar a imagem no formato RGB
    imagem = Image.open(caminho_pgm_entrada)
    imagem = imagem.convert("RGB")  # Garantir que está no modo RGB

    # Inicializar listas para os valores de cada canal
    valores_r = []
    valores_g = []
    valores_b = []

    # Iterar sobre os pixels da imagem para capturar os valores RGB
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            valores_r.append(r)
            valores_g.append(g)
            valores_b.append(b)

    # Criar os histogramas para cada canal
    plt.figure(figsize=(15, 5))
    # Histograma para o canal Red
    plt.subplot(1, 3, 1)
    plt.hist(valores_r, bins=256, color='red', alpha=0.7, edgecolor='black')
    plt.title("Histograma - Canal Red")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")
    plt.grid(True)

    # Histograma para o canal Green
    plt.subplot(1, 3, 2)
    plt.hist(valores_g, bins=256, color='green', alpha=0.7, edgecolor='black')
    plt.title("Histograma - Canal Green")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")
    plt.grid(True)

    # Histograma para o canal Blue
    plt.subplot(1, 3, 3)
    plt.hist(valores_b, bins=256, color='blue', alpha=0.7, edgecolor='black')
    plt.title("Histograma - Canal Blue")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")
    plt.grid(True)

    # Mostrar os histogramas
    plt.tight_layout()
    plt.show()

# Caminhos dos arquivos de entrada e saída
caminho_ppm_entrada = "/home/matias/Documentos/BCC2024-2/PDI/converteBinario/Fig4.ppm"
caminho_p2_saida = "/home/matias/Documentos/BCC2024-2/PDI/Fig4_escala_cinza.pgm"
caminho_p3_saida = "/home/matias/Documentos/BCC2024-2/PDI/RGmax.ppm"
caminho_pgm_entrada = "/home/matias/Documentos/BCC2024-2/PDI/converteBinario/Entrada.pgm"
caminho_pbm_saida = "/home/matias/Documentos/BCC2024-2/PDI/converteBinario/Saida.pbm"
caminho_pgm_negativo = "/home/matias/Documentos/BCC2024-2/PDI/converteBinario/Negativo.pgm"

# Calcular média RGB e salvar imagens P2 e P3
pixels_p2, largura, altura = calcular_media_rgb(caminho_ppm_entrada)

# Cálcula a média RGB e plota no gráfico a distribuição dos tons de cores segundo cada canal
gerar_histograma_rgb(caminho_pgm_entrada)

# Plotar os gráficos
plotar_graficos(pixels_p2, largura, altura)

# Definir o limiar e converter para PBM
limiar = 128
