from PIL import Image
import multiprocessing


def kernel(im, func, kernel_size, kernel_filter):
    """
    Runs the provided callback function for each kernel in the 
    provided image.

    Args
    im: The image to process, type PIL.Image.
    func: The callback function. Needs to take a nested array 
    of pixel rgb tuples as input with the size of kernel_size.
    Needs to accept the optional parameter kernel_filter.
    """
    # Loop through pixels one rectangle at a time.
    for x in range(int(im.size[0]/kernel_size[0])):
        for y in range(int(im.size[1]/kernel_size[1])):
            # Extract pixels in rectangle.
            block = im.crop((x*kernel_size[0], y*kernel_size[1],
                            (x+1)*kernel_size[0], (y+1)*kernel_size[1]))
            pixels = list(block.getdata())

            # Run callback for kernel.
            pixels = func(pixels, kernel_filter, kernel_filter)
            
            # Convert pixels to image for pasting.
            block = Image.new(block.mode, block.size)
            block.putdata(pixels)

            # Paste sorted rectangle to current block location.
            im.paste(block, (x*kernel_size[0], y*kernel_size[1],
                        (x+1)*kernel_size[0], (y+1)*kernel_size[1]))
    
    return im


def kernel_wrapper(im, func, kernel_size, kernel_filter, index, returns):
    """
    Returning values using the multiprocessing library is done using
    shared variables. This method is simply a wrapper which coordinates 
    storing the kernel result.
    """
    returns[index] = kernel(im, func, kernel_size, kernel_filter)


def multikernel(im, func, kernel_size, kernel_filter, threads):
    """
    Splits the provided image into one part for each thread and 
    performs kernel processing on each part with provided callback.
    Returns the combined result as one image.

    Args
    im: The image to process, type PIL.Image.
    func: The callback function, needs to take a nested array of 
    pixel rgb tuples as input.
    """
    # Split image into one part for each thread.
    w,h = im.size
    img = []

    # Determine area to sort for each thread.
    for i in range(threads):
        img.append(im.crop((0, int(h/threads)*i, w, int(h/threads)*(i+1))))
        print( "%i - %i" % (int(h/threads)*i, int(h/threads)*(i+1)) )
   
    manager = multiprocessing.Manager()
    returns = manager.dict()
    jobs = []

    # Start multiprocessing image.
    for i in range(len(img)):
        p = multiprocessing.Process( \
            target=kernel_wrapper, \
            args=(img[i], func, kernel_size, kernel_filter, i, returns))
        p.start()
        jobs.append(p)

    # Wait for all threads to finish processing.
    for i in jobs:
        i.join()

    # Combine processed parts into one final image.
    image = Image.new("RGB", (w, h))
    for i in range(threads):
        image.paste(returns[i], (0, int(h/threads)*i, w, int(h/threads)*(i+1)))
    
    return image
