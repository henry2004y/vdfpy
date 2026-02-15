# Fundamentals of Kinetic Theory

## Phase Space

Consider a particle moving in a one-dimensional space and let the position of the particle be {math}`x = x(t)` and the velocity of the particle be {math}`v = v(t)`. A way to visualize the {math}`x` and {math}`v` trajectories simultaneously is to plot these trajectories parametrically on a two-dimensional graph, where the horizontal coordinate is given by {math}`x(t)` and the vertical coordinate is given by {math}`v(t)`. This x-v plane is called _phase-space_. The trajectory (or orbit) of several particles can be represented as a set of curves in phase-space. Examples of a few qualitatively different phase-space orbits are shown in the following figure.

![Phase-space showing different types of possible particle orbits.](https://henry2004y.github.io/KeyNotes/images/phase_space_trajectories.png){#fig:phase-space}.

Particles in the upper half-plane always move to the right, since they have a positive velocity, while those in the lower half-plane always move to the left. Particles having exact periodic motion (e.g., {math}`x = A\cos t,\, v = −A\sin t`) alternate between moving to the right and the left and so describe an ellipse in phase-space. Particles with quasi-periodic motions will have near-ellipses or spiral orbits. A particle that does not reverse direction is called a passing particle, while a particle confined to a certain region of phase-space (e.g., a particle with periodic motion) is called a trapped particle.

## Distribution Function

The fluid theory is the simplest description of a plasma; it is indeed fortunate that this approximation is sufficiently accurate to describe the majority of observed phenomena. There are some phenomena, however, for which a fluid treatment is inadequate. At any given time, each particle has a specific position and velocity. We can therefore characterize the instantaneous configuration of a large number of particles by specifying the density of particles at each point {math}`x, v` in phase-space. The function prescribing the instantaneous density of particles in phase-space is called the _distribution function_ and is denoted by {math}`f(x, v, t)`. Thus, {math}`f(x, v, t)\mathrm{d}x\mathrm{d}v` is the number of particles at time {math}`t` having positions in the range between {math}`x` and {math}`x+\mathrm{d}x` and velocities in the range between {math}`v` and {math}`v+\mathrm{d}v`. As time progresses, the particle motion and acceleration causes the number of particles in these {math}`x` and {math}`v` ranges to change and so {math}`f` will change. This temporal evolution of {math}`f` gives a description of the system more detailed than a fluid description, but less detailed than following the trajectory of each individual particle. Using the evolution of {math}`f` to characterize the system does not keep track of the trajectories of individual particles, but rather characterizes classes of particles having the same {math}`x, v`.

In fluid theory, the dependent variables are functions of only four independent variables: {math}`x, y, z,` and {math}`t`. This is possible because the velocity distribution of each species is assumed to be Maxwellian everywhere and can therefore be uniquely specified by its bulk velocity {math}`\vec{U}` and the temperature {math}`T`. Since collisions can be rare in high-temperature plasmas, deviations from thermal equilibrium can be maintained for relatively long times. As an example, consider two velocity distributions {math}`f_1(v_x)` and {math}`f_2(v_x)` in a one-dimensional system (figure below). These two distributions will have entirely different behaviors, but as long as the areas under the curves are the same, fluid theory does not distinguish between them.

![Examples of non-Maxwellian distribution functions](https://henry2004y.github.io/KeyNotes/images/distributions_nonmaxwellian_1d.png){#fig-distributions-1d}

When we consider velocity distributions in 3D, we have seven independent variables: {math}`f = f(\mathbf{r}, \mathbf{v}, t)`.
By {math}`f(\mathbf{r}, \mathbf{v}, t)`, we mean that the number of particles per meter cubed at position {math}`\mathbf{r}` and time {math}`t` with velocity components between {math}`v_x` and {math}`v_x + \mathrm{d}v_x`, {math}`v_y` and {math}`v_y + \mathrm{d}v_y`, and {math}`v_z` and {math}`v_z + \mathrm{d}v_z` is

```{math}
:label: vdf3d
f(x, y, z, v_x, v_y, v_z, t) \mathrm{d}v_x \mathrm{d}v_y \mathrm{d}v_z
```

### Moments of the distribution function

![Moments give weighted averages of the particles in the shaded vertical strip.](https://henry2004y.github.io/KeyNotes/images/distribution_moments.png){#fig-distribution-moments}

Let us count the particles in the shaded vertical strip in the above figure. The number of particles in this strip is the number of particles lying between {math}`x` and {math}`x + \mathrm{d}x`, where {math}`x` is the location of the left-hand side of the strip and {math}`x + \mathrm{d}x` is the location of the right-hand side. The number of particles in the strip is equivalently defined as {math}`n(x, t)\mathrm{d}x`, where {math}`n(x)` is the density of particles at {math}`x`. Thus we see that {math}`\int f(x, v)\mathrm{d}v = n(x)` the transition from a phase-space description (i.e., {math}`x, v` are independent variables) to a conventional description (i.e., only {math}`x` is an independent variable) involves “integrating out” the velocity dependence to obtain a quantity (e.g., density) depending only on position. Since the number of particles is finite, and since {math}`f` is a positive quantity, {math}`f` must vanish as {math}`v\rightarrow\pm\infty`.

In three-dimension, the density is now a function of four scalar variables, {math}`n=n(\mathbf{r}, t)`, which is the integral of the distribution function over the velocity space:

```{math}
:label: distribution-density
\begin{aligned}
  n(\mathbf{r}, t) &= \int_{-\infty}^{\infty} \mathrm{d}v_x \int_{-\infty}^{\infty} \mathrm{d}v_y \int_{-\infty}^{\infty} \mathrm{d}v_z f(\mathbf{r}, \mathbf{v}, t) \\
  &= \int_{-\infty}^{\infty}f(\mathbf{r}, \mathbf{v}, t)\mathrm{d}^3v \\
  &= \int_{-\infty}^{\infty}f(\mathbf{r}, \mathbf{v}, t)\mathrm{d}\mathbf{v}
\end{aligned}
```

Note that {math}`\mathrm{d}\mathbf{v}` is not a vector; it stands for a three-dimensional volume element in velocity space. If {math}`f` is normalized so that

```{math}
:label: f_normalization
\int_{-\infty}^{\infty} \hat{f}(\mathbf{r}, \mathbf{v}, t) \mathrm{d}\mathbf{v} = 1
```

Thus

```{math}
:label: f_normalization_dimensionless
\hat{f}(\mathbf{r}, \mathbf{v}, t) = f(\mathbf{r}, \mathbf{v}, t) / n(\mathbf{r}, t)
```

is the probability that a randomly selected particle at position {math}`\mathbf{r}` has the velocity {math}`\mathbf{v}` at time {math}`t`. Using this point of view, we see that averaging over the velocities of all particles at {math}`x` gives the mean velocity

```{math}
:label: distribution-velocity
u(\mathrm{x},t)=\frac{\int\mathbf{v}f(\mathbf{x},\mathbf{v},t)\mathrm{d}\mathbf{v}}{n(\mathbf{x},t)}
```

Similarly, multiplying {math}`\hat{f}` by {math}`mv^2/2` and integrating over velocity will give an expression for the mean kinetic energy of all the particles. This procedure of multiplying {math}`f` by various powers of {math}`\mathbf{v}` and then integrating over velocity is called _taking moments of the distribution function_.

Note that {math}`\hat{f}` is still a function of seven variables, since the shape of the distribution, as well as the density, can change with space and time. From {eq}`f_normalization`, it is clear that {math}`\hat{f}` has the dimensions {math}`(\text{m}/\text{s})^{-3}`; and consequently, from {eq}`f_normalization_dimensionless`, {math}`f` has the dimensions {math}`\text{s}^3 \text{m}^{-6}`.

### Maxwellian Distribution

A particularly important distribution function is the Maxwellian:

```{math}
:label: maxwellian-distribution-normalized
\hat{f}_m = \left(\frac{m}{2\pi k_B T}\right)^{3/2}\exp\left(-\frac{v^2}{v_{th}^2}\right)
```

where

```{math}
v\equiv(v_x^2 + v_y^2 + v_z^2)^{1/2}\quad\text{and}\quad v_{th}\equiv(2k_B T/m)^{1/2}
```

This is the normalized form where {math}`\hat{f}_m` is equivalent to probability: by using the definite integral

```{math}
\int_{-\infty}^{\infty}\exp(-x^2)dx = \sqrt{\pi}
```

one easily verifies that the integral of {math}`\hat{f}_m` over {math}`\mathrm{d}v_x \mathrm{d}v_y \mathrm{d}v_z` is unity.

A common question being asked is:

> Why do we see Maxwellian/Gaussian/normal distribution ubiquitously in nature?

Well, this is related to the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem) in statistics: in many situations, when independent random variables are summed up, their properly normalized sum tends toward a normal distribution even if the original variables themselves are not normally distributed (e.g. a biased coin which give 95% head and 5% tail). In statistical physics, this is related to the fact that a Maxwellian distribution represents the state of a system with the highest entropy under the constraint of energy conservation.

There are several average velocities of a Maxwellian distribution that are commonly used. The root-mean-square velocity is given by

```{math}
(\overline{v^2})^{1/2} = (3k_B T/m)^{1/2}
```

The average magnitude of the velocity {math}`|v|`, or simply {math}`\bar{v}`, is found as follows:

```{math}
\bar{v} = \int_{-\infty}^{\infty}v\hat{f}(\mathbf{v})d^3v
```

Since {math}`\hat{f}_m` is isotropic, the integral is most easily done in spherical coordinates in v space. Since the volume element of each spherical shell is {math}`4\pi v^2 \mathrm{d}v`, we have

```{math}
\begin{aligned}
  \bar{v} &= (m/2\pi k_B T)^{3/2}\int_0^\infty v[\exp(-v^2/v_{th}^2)]4\pi v^2 \mathrm{d}v \\
  &= (\pi v_{th}^2)^{-3/2} 4\pi v_{th}^4 \int_0^\infty [\exp(-y^2)]y^3 dy
\end{aligned}
```

The definite integral has a value 1/2, found by integration by parts. Thus

```{math}
\bar{v} = 2\sqrt{\pi}v_{th} = 2(2k_B T/\pi m)^{1/2}
```

The velocity component in a _single direction_, say {math}`v_x`, has a different average. Of course, {math}`\bar{v}_x` vanishes for an isotropic distribution; but {math}`|\bar{v}_x|` does not:

```{math}
|\bar{v}_x| = \int |v_x|\hat{f}_m(\mathbf{v})\mathrm{d}^3 v = \pi^{-1/2}v_{th} = (2k_B T/\pi m)^{1/2}
```

To summarize: for a Maxwellian,

```{math}
\begin{aligned}
  v_{rms} &= (3k_B T/m)^{1/2} \\
  |\bar{v}| &= 2(2k_B T/\pi m)^{1/2} \\
  |\bar{v}_x| &= (2k_B T/\pi m)^{1/2} \\
  \bar{v}_x &= 0
\end{aligned}
```

For an isotropic distribution like a Maxwellian, we can define another function {math}`g(v)` which is a function of the scalar magnitude of {math}`\mathbf{v}` such that

```{math}
\int_0^\infty g(v) \mathrm{d}v = \int_{-\infty}^{\infty} f(\mathbf{v})\mathrm{d}v
```

For a Maxwellian, we see that

```{math}
:label: g_dist
g(v) = 4\pi n (m/2\pi k_B T)^{3/2} v^2 \exp(-v^2/v_{th}^2)
```

Note the difference between {math}`g(v)` and a one-dimensional Maxwellian distribution {math}`f(v_x)`. Although {math}`f(v_x)` is maximum for {math}`v_x=0`, {math}`g(v)` is zero for {math}`v=0`. This is just a consequence of the vanishing of the volume in phase space for {math}`v=0`. Sometimes {math}`g(v)` is carelessly denoted by {math}`f(v)`, as distinct from {math}`f(\mathbf{v})`; but {math}`g(v)` is a different function of its argument than {math}`f(\mathbf{v})` is of its argument. From {eq}`g_dist`, it is clear that {math}`g(v)` has dimensions {math}`\text{s}/\text{m}^4`.

## Gallery

* Isotropic Maxwellian distribution

```{math}
\hat{f}_m = \left(\frac{m}{2\pi k_B T}\right)^{3/2}\exp\left(-\frac{v^2}{v_{th}^2}\right)
```

* Anisotropic (pancake) distribution

```{math}
f(v_\perp, v_\parallel) = \frac{n}{T_\perp T_\parallel^{1/2}}\Big( \frac{m}{2\pi k_B} \Big)^{3/2} \exp\Big( -\frac{mv_\perp^2}{2k_B T_\perp} - \frac{m(v_\parallel - v_{0\parallel})^2}{2k_B T_\parallel} \Big)
```

* Beam

* Crescent shape
