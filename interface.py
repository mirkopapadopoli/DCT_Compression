import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import os, cv2

# Utilizzo cv2 che calcola la DCT2 utilizzando una versione ottimizzata dell'algoritmo,
def apply_dct2(image):
    return cv2.dct(np.float32(image))

# DCT2 inversa, ricostruisce l'immagine dopo l'applicazione della DCT2 e il taglio delle frequenze.
def apply_inverse_dct2(coefficients):
    return cv2.idct(coefficients)

# Elimina i coefficienti delle frequenze indesiderate al di sopra di una determinata soglia.
def threshold_cutoff(coefficients, threshold):
    size = coefficients.shape[0]
    for i in range(size):
        for j in range(size):
            if i + j >= threshold:
                coefficients[i, j] = 0
    return coefficients

# Calcola il numero di blocchi da creare
def num_blocks(height, width, block_size):
    num_blocks_height = height // block_size
    num_blocks_width = width // block_size
    return num_blocks_height, num_blocks_width

# Calcola le dimensioni dell'immagine
def calculate_dimension_image(height, width, block_size):
    num_blocks_height, num_blocks_width = num_blocks(height, width, block_size)
    actual_height = num_blocks_height * block_size
    actual_width = num_blocks_width * block_size
    return actual_height, actual_width

# Ritaglia l'immagine alla dimensione effettiva
def divide_image_in_blocks(image, num_blocks_height, num_blocks_width):
    blocks = np.split(image, num_blocks_height, axis=0)
    blocks = [np.split(block, num_blocks_width, axis=1) for block in blocks]
    blocks = np.array(blocks)
    return blocks

# Processo e utilizzo di funzioni precedenti
def run_process_block(blocks, block_size, threshold):
    num_blocks_height, num_blocks_width = blocks.shape[0], blocks.shape[1]
    for i in range(num_blocks_height):
        for j in range(num_blocks_width):
            block = blocks[i, j]

            # Applica la DCT2
            coefficients = apply_dct2(block)

            # Taglia le frequenze
            coefficients = threshold_cutoff(coefficients, threshold)

            # Applica l'inversa della DCT2
            reconstructed_block = apply_inverse_dct2(coefficients)

            # Arrotonda e normalizza i valori
            reconstructed_block = np.round(reconstructed_block)
            reconstructed_block = np.clip(reconstructed_block, 0, 255)

            # Aggiorna il blocco ricostruito
            blocks[i, j] = reconstructed_block
    return blocks

# Ricostruisce l'immagine a partire dai blocchi
def image_dimension(image):
    height, width = image.shape
    return height, width

# Salva l'immagine ricostruita
def save_disk_image(reconstructed_image):
    img_path = "/Users/mirkopapadopoli/Code/DCT/img_reconstructed/"
    output_path = img_path + selected_image_path.split('/')[-1] + "_reconstructed.bmp"
    Image.fromarray(reconstructed_image).save(output_path)
    return output_path

# Calcola la dimensione dell'immagine ricostruita
def reconstruction_dimension_image(image):
    output_path = save_disk_image(image)
    file_size_kb = os.path.getsize(output_path) / 1024
    file_size_kb_original = os.path.getsize(selected_image_path) / 1024
    return file_size_kb, file_size_kb_original

# Stampa l'immagine originale e l'immagine ricostruita
def print_original_reconstructed_image(image, reconstructed_image):
    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(image, cmap='gray')
    axs[0].set_title('Original Image')
    axs[1].imshow(reconstructed_image, cmap='gray')
    axs[1].set_title('Reconstructed Image')
    plt.show()

# Carica l'immagine
def upload_image():
    global selected_image_path, window, block_size_entry, threshold_entry, image_label
    image = np.asarray(Image.open(selected_image_path).convert('L'))
    if len(image.shape) > 2:
        # Carica l'immagine in toni di grigio
        image = cv2.imread(selected_image_path, 0)
    return image

# Run
def process_image():
    # global selected_image_path, window, block_size_entry, threshold_entry, image_label
    # image = np.asarray(Image.open(selected_image_path).convert('L'))
    # if len(image.shape) > 2:
    #     # Carica l'immagine in toni di grigio
    #     image = cv2.imread(selected_image_path, 0)
    image = upload_image()
    # Calcola le dimensioni dell'immagine
    #height, width = image.shape
    height, width = image_dimension(image)

    block_size = int(block_size_entry.get())
    threshold = int(threshold_entry.get())

    # Calcola il numero di blocchi da creare
    # num_blocks_height = height // block_size
    # num_blocks_width = width // block_size
    num_blocks_height, num_blocks_width = num_blocks(height, width, block_size)

    # Calcola la dimensione effettiva dell'immagine
    # actual_height = num_blocks_height * block_size
    # actual_width = num_blocks_width * block_size
    actual_height, actual_width = calculate_dimension_image(height, width, block_size)

    # Ritaglia l'immagine alla dimensione effettiva
    image2 = image[:actual_height, :actual_width]

    # Suddivide l'immagine in blocchi
    # blocks = np.split(image2, num_blocks_height, axis=0)
    # blocks = [np.split(block, num_blocks_width, axis=1) for block in blocks]
    # blocks = np.array(blocks)
    blocks = divide_image_in_blocks(image2, num_blocks_height, num_blocks_width)

    # Applica il processo a ciascun blocco
    # for i in range(num_blocks_height):
    #     for j in range(num_blocks_width):
    #         block = blocks[i, j]

    #         # Applica la DCT2
    #         coefficients = apply_dct2(block)

    #         # Taglia le frequenze
    #         coefficients = threshold_cutoff(coefficients, threshold)

    #         # Applica l'inversa della DCT2
    #         reconstructed_block = apply_inverse_dct2(coefficients)

    #         # Arrotonda e normalizza i valori
    #         reconstructed_block = np.round(reconstructed_block)
    #         reconstructed_block = np.clip(reconstructed_block, 0, 255)

    #         # Aggiorna il blocco ricostruito
    #         blocks[i, j] = reconstructed_block
    blocks = run_process_block(blocks, block_size, threshold)

    # Ricompone l'immagine a partire dai blocchi
    reconstructed_image = np.block([[block for block in row] for row in blocks])

    # Converte l'immagine in formato byte
    reconstructed_image = reconstructed_image.astype(np.uint8)

    # Salva l'immagine ricostruita su disco
    # output_path = "reconstructed_image.bmp"
    # Image.fromarray(reconstructed_image).save(output_path)
    output_path = save_disk_image(reconstructed_image)

    # Calcola la dimensione dell'immagine ricostruita in KB
    #file_size_kb = os.path.getsize(output_path) / 1024
    #file_size_kb_original = os.path.getsize(selected_image_path) / 1024
    file_size_kb_original, file_size_kb = reconstruction_dimension_image(image)

    # Visualizza la dimensione dell'immagine ricostruita
    print(f"Dimensione dell'immagine originale: {file_size_kb_original:.2f} KB")
    print(f"Dimensione dell'immagine ricostruita: {file_size_kb:.2f} KB")

    print("Shape immagine originale:", image.shape)
    print("Shape immagine ricostruita:", reconstructed_image.shape)

    # Visualizza l'immagine originale e l'immagine ricostruita affiancate
    # fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    # axes[0].imshow(image, cmap='gray')
    # axes[0].set_title("Immagine originale")
    # axes[0].axis('off')
    # axes[1].imshow(reconstructed_image, cmap='gray')
    # axes[1].set_title("Immagine ricostruita")
    # axes[1].axis('off')
    # plt.show()
    print_original_reconstructed_image(image, reconstructed_image)


def choose_image():
    global selected_image_path, image_label

    selected_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.bmp")])
    selected_image = Image.open(selected_image_path)

    max_width = 400  # Larghezza massima desiderata
    max_height = 400  # Altezza massima desiderata

    # Ridimensiona l'immagine proporzionalmente
    new_width, new_height = proportionally_resize(selected_image.width, selected_image.height, max_width, max_height)
    resized_image = selected_image.resize((new_width, new_height))

    selected_image_tk = ImageTk.PhotoImage(resized_image)
    image_label.configure(image=selected_image_tk)
    image_label.image = selected_image_tk

    image_loaded = True

def proportionally_resize(width, height, max_width, max_height):
    if width > height:
        new_width = max_width
        new_height = int(height * max_width / width)
    else:
        new_width = int(width * max_height / height)
        new_height = max_height
    return new_width, new_height

def reset_variables():
    global selected_image_path, block_size_entry, threshold_entry, image_label

    selected_image_path = ""
    block_size_entry.delete(0, tk.END)
    threshold_entry.delete(0, tk.END)
    image_label.configure(image=None)
    image_label.image = None

def create_interface():
    global selected_image_path, window, block_size_entry, threshold_entry, image_label

    window = tk.Tk()
    window.title("Image Processing")
    window.geometry("600x600")
    window.configure(bg="#FFFFFF")

    frame_form = tk.Frame(window, bg="#D9D9D9")
    frame_form.pack(pady=20, padx=20)

    choose_image_button = tk.Button(frame_form, text="Carica Immagine", command=choose_image, width=18, bg="#D9D9D9", fg="black")
    label_block_size = tk.Label(frame_form, text="Ampiezza finestre (F):", width=18, bg="#D9D9D9", fg="black")
    label_threshold = tk.Label(frame_form, text="Soglia di taglio (d):", width=18, bg="#D9D9D9", fg="black")

    run_button = tk.Button(frame_form, text="Elabora Immagine", command=process_image, width=18, bg="#D9D9D9", fg="green")
    reset_button = tk.Button(frame_form, text="Reset", command=reset_variables, width=18, bg="#D9D9D9", fg="red")

    choose_image_button.grid(row=0, column=0, pady=15)
    label_block_size.grid(row=1, column=0, pady=5)
    label_threshold.grid(row=2, column=0, pady=5)

    block_size_entry = tk.Entry(frame_form, bg="#6E7480", fg="white")
    threshold_entry = tk.Entry(frame_form, bg="#6E7480", fg="white")

    block_size_entry.grid(row=1, column=1, pady=5, padx=10)
    threshold_entry.grid(row=2, column=1, pady=5, padx=10)

    run_button.grid(row=3, columnspan=2, pady=10)
    reset_button.grid(row=4, columnspan=2, pady=10)

    frame_image = tk.Frame(window, bg="#D9D9D9")
    frame_image.pack(pady=20)
        
    image_label = tk.Label(frame_image, bg="#D9D9D9")
    image_label.grid(row=0, pady=5)

    selected_image_label = tk.Label(frame_image, text="", bg="#D9D9D9")
    selected_image_label.grid(row=1, pady=5)

    window.mainloop()



if __name__ == "__main__":
    create_interface()
