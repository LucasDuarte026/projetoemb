import cv2
import collections
import numpy as np
import time

# ========== CONFIGURAÇÕES ==========
CAMERA_INDEX = 0
FPS = 30
BUFFER_DURATION_SECONDS = 15
MAX_FRAMES = int(FPS * 15)
FOURCC_CODEC = 'mp4v'
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
MIN_HAND_AREA = 3000  # Área mínima para considerar mão

# Buffer circular
frame_buffer = collections.deque(maxlen=MAX_FRAMES)

def detect_hand(frame):
    """Detecta uma mão usando segmentação por cor de pele e retorna centro e contorno."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, mask

    # Pega o maior contorno
    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < MIN_HAND_AREA:
        return None, None, mask

    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None, None, mask
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy), largest, mask

def save_buffer_to_video(buffer, output_file, fps, frame_size):
    """Salva o buffer de frames em arquivo de vídeo."""
    fourcc = cv2.VideoWriter_fourcc(*FOURCC_CODEC)
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)
    if not out.isOpened():
        print(f"❌ Erro ao criar vídeo {output_file}")
        return False
    for frame in buffer:
        out.write(frame)
    out.release()
    duracao = len(buffer) / fps
    print(f"✅ Vídeo salvo: {output_file} ({duracao:.2f}s)")
    return True

def run_capture_loop():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print("🎥 Captura iniciada. Pressione 'q' para sair.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            center, contour, mask = detect_hand(frame)
            if contour is not None:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, center, 10, (255, 0, 0), -1)
                cv2.putText(frame, "Mao detectada", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Salvar somente se buffer tiver 15s completos
                if len(frame_buffer) >= MAX_FRAMES:
                    output_file = f"mao_capturada_{time.strftime('%Y%m%d_%H%M%S')}.mp4"
                    save_buffer_to_video(frame_buffer, output_file, FPS, frame_size)
                    frame_buffer.clear()

            frame_buffer.append(frame.copy())
            buffer_pct = int((len(frame_buffer) / MAX_FRAMES) * 100)
            cv2.putText(frame, f"Buffer: {len(frame_buffer)}/{MAX_FRAMES} ({buffer_pct}%)",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Detector de Mao", frame)
            cv2.imshow("Deteccao de Pele", mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Recursos liberados.")

if __name__ == "__main__":
    run_capture_loop()
