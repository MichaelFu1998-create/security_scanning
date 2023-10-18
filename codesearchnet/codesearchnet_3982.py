def plot_curves(i_batch, adv_loss, gen_loss, l1_reg, cols):
    """Plot SAM's various losses."""
    from matplotlib import pyplot as plt
    if i_batch == 0:
        try:
            ax.clear()
            ax.plot(range(len(adv_plt)), adv_plt, "r-",
                    linewidth=1.5, markersize=4,
                    label="Discriminator")
            ax.plot(range(len(adv_plt)), gen_plt, "g-", linewidth=1.5,
                    markersize=4, label="Generators")
            ax.plot(range(len(adv_plt)), l1_plt, "b-",
                    linewidth=1.5, markersize=4,
                    label="L1-Regularization")
            plt.legend()

            adv_plt.append(adv_loss.cpu().data[0])
            gen_plt.append(gen_loss.cpu().data[0] / cols)
            l1_plt.append(l1_reg.cpu().data[0])

            plt.pause(0.0001)

        except NameError:
            plt.ion()
            fig, ax = plt.figure()
            plt.xlabel("Epoch")
            plt.ylabel("Losses")

            plt.pause(0.0001)

            adv_plt = [adv_loss.cpu().data[0]]
            gen_plt = [gen_loss.cpu().data[0] / cols]
            l1_plt = [l1_reg.cpu().data[0]]

    else:
        adv_plt.append(adv_loss.cpu().data[0])
        gen_plt.append(gen_loss.cpu().data[0] / cols)
        l1_plt.append(l1_reg.cpu().data[0])