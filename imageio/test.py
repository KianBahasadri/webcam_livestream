import imageio as iio
import matplotlib.pyplot as plt
camera = iio.get_reader("<video0>")
photo = camera.get_data(0)
camera.close()
plt.imshow(photo)

