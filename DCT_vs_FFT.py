import numpy as np
import time
import matplotlib.pyplot as plt

def my_dct2(image_block):

    M, N = image_block.shape
    dct_result = np.zeros((M, N))

    for i in range(M):
        for j in range(N):
            alpha_i = 1 if (i == 0) else (np.sqrt(M))
            alpha_j = 1 if (j == 0) else (np.sqrt(N))
            sum_value = 0

            for x in range(M):
                for y in range(N):
                    cos_u = np.cos(((2 * x + 1) * i * np.pi) / (2 * M))
                    cos_v = np.cos(((2 * y + 1) * j * np.pi) / (2 * N))
                    sum_value += image_block[x, y] * cos_u * cos_v

            dct_result[i, j] = alpha_i * alpha_j * sum_value / np.sqrt(M * N)

    return dct_result

def generate_image(N):
     return np.random.rand(N, N)


def main():
    N_values = [2, 4, 8, 16, 32, 64]
    times_dct2_homemade = []
    times_dct2_library = []

    for N in N_values:
        image_block = generate_image(N)

        # DCT2 fatta in casa
        start_time_homemade = time.time()
        dct_result_homemade = my_dct2(image_block)
        end_time_homemade = time.time()
        times_dct2_homemade.append(end_time_homemade - start_time_homemade)

        # DCT2 con FFT
        start_time_fast = time.time()
        dct_result_fast = np.fft.fft2(image_block, norm='ortho')
        end_time_fast = time.time()
        times_dct2_library.append(end_time_fast - start_time_fast)

    # Plot dei tempi di esecuzione
    plt.semilogy(N_values, times_dct2_homemade, label='DCT2 Homemade')
    plt.semilogy(N_values, times_dct2_library, label='DCT2 FFT)')
    plt.xlabel('Dimensione N')
    plt.ylabel('Tempo di esecuzione (sec)')
    plt.title('Confronto dei tempi di esecuzione DCT2 personalizzata vs DCT2 libreria FFT')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
