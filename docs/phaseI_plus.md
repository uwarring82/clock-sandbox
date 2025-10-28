# Phase I+ Notes: Additional Clocks and Triangular Consensus

## New clock types
- **RandomWalkFreqClock**: fractional frequency executes a random walk; suitable for modeling long-term diffusion processes.
- **FlickerLikeFreqClock**: simple IIR-based approximation to flicker-like fractional-frequency noise (pedagogical; not a full power-law synthesizer).

## Pairwise comparisons
Each noisy clock can be compared against the IdealClock via:
- `run_clocks([...], duration, dt)` → time-series
- `compare_clocks(time, ideal, noisy)` → metrics (mean offset, std, max abs, final drift rate)

## Triangular consensus
Given three noisy clocks $C_1, C_2, C_3$, we compute an inverse-variance weighted average:
\[
C_{\text{cons}}(t) = \sum_i w_i\, C_i(t), \quad w_i \propto \frac{1}{\operatorname{Var}[C_i(t)-\langle C_i\rangle]}
\]
This provides a simple "triangular check" that reduces variance under the assumption of uncorrelated errors.
Compare $C_{\text{cons}}$ to the IdealClock using `compare_clocks(...)`.

**Caveat:** This is a pedagogical proxy. For rigorous metrology, one would use Allan/MDEV-based estimators and account for correlations and time-dependent variances.
