from .ansirgb import ansirgb

def gradient(text:str, mode:str, start_color:list, end_color:list, usenumpy:bool=False):
    # If usenumpy is True, the numpy module is required.
    
    # Example usage:
    # gradient(text="Text", mode="by-character-diagonal", start_color=[0, 0, 0], end_color=[255, 255, 255])

    # Notes:
    # text          must be a string        any content
    # mode          must be a string        its content can only be "by-character", "by-character-diagonal", "line-horizontal" or "line-vertical"
    # start_color   must be a list          its content must be [int>0<255, int>0<255, int>0<255]
    # end_color     must be a list          its content must be [int>0<255, int>0<255, int>0<255]
    # usenumpy      must be a bool          its content must be True (default) or False
    
    class InvalidRGBColor(Exception):
        def __init__(self, reason=None):
            self.reason = reason
            message = "The RGB value must be higher than 0 and lower than 255. Your input doesn't match those requirements."
    
    class InvalidGradientOption(Exception):
        def __init__(self, reason=None):
            self.reason = reason
            message = f"The gradient option you chose ({str(reason)}) is not a valid option."
    
    class InvalidStepsAmount(Exception):
        def __init__(self, reason=None):
            self.reason = reason
            message = "The amount of steps for the gradient must be integer and higher than 0."
    
    def rgb(r:int=0, g:int=0, b:int=0):
        return f"\x1b[38;2;{r};{g};{b}m"
    
    def generate_rgb_grad(start_color, end_color, steps, un=usenumpy):

        def validate_rgb_color(color):
            for channel in color:
                if not 0 <= channel <= 255:
                    raise InvalidRGBColor("RGB color values should be between 0 and 255")
        
        validate_rgb_color(start_color)
        validate_rgb_color(end_color)
        
        if un:
            try:
                import numpy as np
            except ImportError:
                import sys
                import platform
                
                if platform.system() == "Windows":
                    python_command = "python"  # Windows ussually has Python in PATH
                else:
                    python_command = sys.executable or "python"
                
                print(f"Numpy module is not installed.\nInstall it by running \"{python_command} -m pip install numpy\" or disable it.")
            if steps <= 0:
                raise InvalidStepsAmount("The amount of steps must be higher than 0")
            s_color = np.array(start_color)
            e_color = np.array(end_color)
            delta_color = (e_color - s_color) / steps
            gradient = np.round(np.arange(steps + 1)[:, np.newaxis] * delta_color + s_color).clip(0, 255).astype(int)
            return gradient.tolist()
        else:
            if steps <= 0:
                raise InvalidStepsAmount("The amount of steps must be higher than 0")
            # Calculate the difference between the start and the end values for each RGB component
            delta_r = (end_color[0] - start_color[0]) / steps
            delta_g = (end_color[1] - start_color[1]) / steps
            delta_b = (end_color[2] - start_color[2]) / steps
            # Generate the gradient
            gradient = []
            for i in range(steps + 1):
                # Calculate the RGB values for the current step
                r = round(start_color[0] + i * delta_r)
                g = round(start_color[1] + i * delta_g)
                b = round(start_color[2] + i * delta_b)
                # Make sure the values are in range [0, 255]
                r = min(255, max(0, r))
                g = min(255, max(0, g))
                b = min(255, max(0, b))
                # Add the values to the gradient list
                gradient.append([r, g, b])
            return gradient
        
    if mode == "by-character":
        t = list(text)
        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=len(t)-1)
        i = 0
        for character in t:
            print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
            i = i + 1
    elif mode == "by-character-diagonal":
        t = list(text)
        if "\n" in t:
            li = text.split("\n")
        t.append("\n")
        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=(len(text.split("\n")[0]) + text.count("\n")) if (text and "\n" in text) else None)
        i = 0
        o = 0
        if li:
            for line in li:
                i = i + o
                for character in line:
                    print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                    i = i + 1
                o = o + 1
                if o < len(li):
                    print("\033[0m", end='\n')
                    i = 0
        else:
            for character in t:
                print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                i = i + 1
    elif mode == "line-vertical":
        t = list(text)
        if "\n" in t:
            li = text.split("\n")
        t.append("\n")
        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=(len(text.split("\n")[0]) + text.count("\n")) if (text and "\n" in text) else None)
        i = 0
        o = 0
        if li:
            for line in li:
                for character in line:
                    print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                    i = i + 1
                o = o + 1
                if o < len(li):
                    print("\033[0m", end='\n')
                    i = 0
        else:
            for character in t:
                print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                i = i + 1
    elif mode == "line-horizontal":
        t = text.split("\n")

        # Remove the last "\n"
        tc = len(t) - 1 if t[-1] == "\n" else len(t)
        c = 0
        tt = []
        while tc > 0:
            tt.append(t[c])
            c += 1
            tc += -1
        t = tt

        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=len(t)-1)
        i = 0
        for line in t:
            print(f"{rgb(l[i][0], l[i][1], l[i][2])}{line}", end='\n')
            i = i + 1
    else:
        raise InvalidGradientOption("The gradient option you chose (%s) doesn't exist." % mode)
    
    # End any remaining color
    print("\033[0m", end='')