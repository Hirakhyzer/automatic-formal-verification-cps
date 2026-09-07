def plot_flowpipe_2d(flowpipe, dims=(0, 1), ax=None):
    """Optional matplotlib visualization; not part of the verification proof."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    if ax is None:
        _, ax = plt.subplots()
    for item in flowpipe.sets:
        s = item.set.interval_hull() if hasattr(item.set, "interval_hull") else item.set
        x0, y0 = s.lower[dims[0]], s.lower[dims[1]]
        w, h = s.upper[dims[0]] - x0, s.upper[dims[1]] - y0
        ax.add_patch(Rectangle((x0, y0), w, h, fill=False, alpha=0.35))
    ax.autoscale()
    return ax
