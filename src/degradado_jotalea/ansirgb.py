def ansirgb(r:int=0, g:int=0, b:int=0):
    return f"\x1b[38;2;{r};{g};{b}m"