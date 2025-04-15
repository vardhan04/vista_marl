def export_as_gif(frames, filename):
    import imageio
    imageio.mimsave(filename, frames, fps=2)
