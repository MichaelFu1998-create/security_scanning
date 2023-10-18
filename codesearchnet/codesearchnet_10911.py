def _generate(num_particles, D, box, rs):
        """Generate a list of `Particle` objects."""
        X0 = rs.rand(num_particles) * (box.x2 - box.x1) + box.x1
        Y0 = rs.rand(num_particles) * (box.y2 - box.y1) + box.y1
        Z0 = rs.rand(num_particles) * (box.z2 - box.z1) + box.z1
        return [Particle(D=D, x0=x0, y0=y0, z0=z0)
                for x0, y0, z0 in zip(X0, Y0, Z0)]