import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path

class UIHandler:
    def __init__(self):
        self.number_positions = {}  # To store number-to-coordinate mapping
    
    def display_numbered_overlay(self):
        """Capture the screen, detect text, and overlay numbers on each detected element."""
        try:
            screenshot = ImageGrab.grab()
            image = np.array(screenshot)
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

            self.number_positions.clear()
            overlay = image.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_color = (0, 255, 0)  # Green for visibility
            thickness = 2

            number = 1  # Start numbering elements
            for i in range(len(data['Core'])):
                text = data['Core'][i].strip()
                if text:  # Non-empty text
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    center_x, center_y = x + w // 2, y + h // 2

                    # Overlay number near the detected text
                    cv2.putText(overlay, str(number), (x, y - 5), font, font_scale, font_color, thickness)
                    cv2.rectangle(overlay, (x, y), (x + w, y + h), font_color, 1)

                    # Store number-to-position mapping
                    self.number_positions[number] = (center_x, center_y)
                    number += 1
            
            # Display the overlay
            cv2.imshow("Numbered Elements", cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"An error occurred: {e}")

    def click_on_number(self, number):
        """Click on a specific numbered element."""
        if number in self.number_positions:
            x, y = self.number_positions[number]
            pyautogui.click(x, y)
            print(f"Clicked on element {number} at position ({x}, {y}).")
        else:
            print(f"Number {number} not found.")

# Test the functionality
def main():
    ui_handler = UIHandler()
    
    # Step 1: Display numbered overlay
    print("Displaying numbered overlay. Press any key to continue.")
    ui_handler.display_numbered_overlay()
    
    # Step 2: Demonstrate clicking
    try:
        number_to_click = int(input("Enter the number of the element you want to click: "))
        ui_handler.click_on_number(number_to_click)
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()