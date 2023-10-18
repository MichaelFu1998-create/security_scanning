def _saliency_map(self, a, image, target, labels, mask, fast=False):
        """Implements Algorithm 3 in manuscript

        """

        # pixel influence on target class
        alphas = a.gradient(image, target) * mask

        # pixel influence on sum of residual classes
        # (don't evaluate if fast == True)
        if fast:
            betas = -np.ones_like(alphas)
        else:
            betas = np.sum([
                a.gradient(image, label) * mask - alphas
                for label in labels], 0)

        # compute saliency map
        # (take into account both pos. & neg. perturbations)
        salmap = np.abs(alphas) * np.abs(betas) * np.sign(alphas * betas)

        # find optimal pixel & direction of perturbation
        idx = np.argmin(salmap)
        idx = np.unravel_index(idx, mask.shape)
        pix_sign = np.sign(alphas)[idx]

        return idx, pix_sign