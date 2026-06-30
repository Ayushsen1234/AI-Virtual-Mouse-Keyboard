import cv2

keys = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M"],
    ["SPACE","BACKSPACE","ENTER"]
]


class Button:
    def __init__(self, pos, text, size=[70, 70]):
        self.pos = pos
        self.text = text
        self.size = size


def draw_keyboard(img, button_list):
    for button in button_list:

        x, y = button.pos
        w, h = button.size

        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (255, 0, 255), cv2.FILLED)

        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (255, 255, 255), 2)

        cv2.putText(img, button.text,
                    (x + 20, y + 45),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (255, 255, 255),
                    2)

    return img
def create_buttons():
    button_list = []

    key_width = 80
    key_height = 80
    gap = 10

    # Row 1
    y = 450
    for i, key in enumerate(keys[0]):
        x = 80 + i * (key_width + gap)
        button_list.append(Button((x, y), key, [key_width, key_height]))

    # Row 2
    y = 540
    for i, key in enumerate(keys[1]):
        x = 120 + i * (key_width + gap)
        button_list.append(Button((x, y), key, [key_width, key_height]))

    # Row 3
    y = 630
    for i, key in enumerate(keys[2]):
        x = 200 + i * (key_width + gap)
        button_list.append(Button((x, y), key, [key_width, key_height]))

    # Bottom Row
    y = 720

    button_list.append(Button((80, y), "SPACE", [350, 80]))
    button_list.append(Button((450, y), "BACKSPACE", [220, 80]))
    button_list.append(Button((690, y), "ENTER", [180, 80]))

    return button_list