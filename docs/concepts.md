# Concepts (Phase I)

- **Elapsed time (seconds)** since epoch \(t_0 = 0\).
- **Fractional frequency** \( y(t) \) is dimensionless; Phase I implements white \(y\) with RMS \(\sigma_y(\tau=1\text{ s})\).
- **Why drift appears:** integrating \( 1 + y_k \) over time accumulates stochastic error.
- **Comparison metrics:** mean offset, standard deviation, max absolute error, final drift rate.
- Next phases: Allan deviation, flicker and random-walk frequency noise, disciplining (PLL), GNSS/VLBI/pulsar adapters.

References: NIST Time and Frequency Division notes; BIPM CCTF materials (to be added in Phase II docs).
