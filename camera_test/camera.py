import cv2
import numpy as np
cap = cv2.VideoCapture(2)  # Numer kamery - 0 oznacza domyślną kamerę

# Pobranie rozmiarów obrazu z kamery
ret, frame = cap.read()
height, width, _ = frame.shape

# Obliczenie rozmiarów i pozycji połowy obrazu
half_width = width // 2
half_height = height // 2

# Główna pętla programu
while True:
    # Odczytanie obrazu z kamery
    ret, frame = cap.read()

    # Przycięcie obrazu do połowy
    half_frame_gora = frame[:half_height, :, :]
    half_frame_dol_lewo = frame[half_height:, :half_width, :]
    half_frame_dol_prawo = frame[half_height:, half_width:, :]

    combined_horizontal = np.concatenate((half_frame_dol_prawo, half_frame_gora, half_frame_dol_lewo), axis=1)
    # resized = cv2.resize(combined_horizontal, (height//2, width//2))
    # Wyświetlenie obrazu
    cv2.imshow('Half Frame', combined_horizontal)

    # Wyjście z pętli po naciśnięciu klawisza 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()