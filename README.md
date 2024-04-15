# Mixed layer heat budget analysis of ACCESS-OM2 runs

This notebook contains a quick analysis of the mixed layer heat budget in ACCESS-OM2, using online heat budget diagnostics, including the computation of the entrainment term.

## Background Theory and diagnostics

### ACCESS-OM2 "Eulerian" heat budget

\begin{align}
  \textit{temp\_tendency} = &\textit{temp\_advection} + \\ &\quad +
  \textit{temp\_submeso} \\ &\quad + \textit{temp\_vdiffuse\_diff\_cbt}  + \textit{temp\_nonlocal\_KPP} \\ &\quad + \textit{sw\_heat} +
  \textit{temp\_rivermix} + \textit{temp\_vdiffuse\_sbc} + \textit{sfc\_hflux\_pme} \\
  & \quad + \textit{frazil\_3d}\\ 
   & \quad + \textit{temp\_vdiffuse\_k33} + \textit{neutral\_diffusion\_temp}\\
   & \quad + \textit{neutral\_gm\_temp} \\
   & \quad + \textit{mixdownslope\_temp} + \textit{temp\_sigma\_diff} + \textit{temp\_eta\_smooth}
\end{align}

All terms are in units of Wm$^{-2}$ - i.e. the tendency of the heat content within each grid cell per unit area, $\rho_0 C_p\Theta \Delta z$, where $\Delta z$ is the time variable grid cell thickness, $\rho_0=1035$kgm$^{-3}$ is the reference density, $C_p=3992.10322329649$Jkg$^{-1}$$^\circ$C$^{-1}$ is the specific heat and $\Theta$ is Conservative Temperature.

- temp\_tendency is the tendency term
- temp\_advection is the convergence of the three-dimensional resolved advection (this can be split into components by taking the convergence of the temp\_xflux\_adv, temp\_yflux\_adv and temp\_zflux\_adv terms)
- temp\_submeso is the convergence of the three-dimensional parameterized submesoscale advection (pretty small).
- temp\_vdiffuse\_diff\_cbt and temp\_nonlocal\_KPP are the vertical mixing terms.
- The next line contains all of the surface heat flux terms. Note that sw\_heat is a three-dimensional term that *redistributes* the impact of SW radiation from the surface layer into the interior (i.e. it is negative in the surface layer and positive below, summing to zero). temp\_rivermix is also three-dimensional as the impact of river runoff is spread over a few layers (4 I think). The other terms are two-dimensional (only non-zero in the surface layer).
- frazil\_3d is the formation of frazil ice
- temp\_vdiffuse\_k33 and neutral\_diffusion\_temp are parameterized along-isopycnal mixing (might not be on in all configurations, e.g. ACCESS-OM2-01).
- neutral\_gm\_temp is parameterization advection by mesoscale eddies
- The last line includes some miscellaneous mixing terms (all pretty small).

Also see https://github.com/COSIMA/access-om2/issues/139#issuecomment-639278547 for a discussion of the surface heat flux terms in ACCESS-OM2/CM2.

### Mixed layer temperature budget 

At each grid cell write the model heat budget above as

$$\frac{\partial (\rho_0 C_p \Theta \Delta z)}{\partial t} = \textit{temp\_tendency} = \sum_i P_i$$

Where $P_i$ are the RHS processes. Units are Wm$^{-2}$. Summing (where we use an integral sign for simplicity) over a mixed layer of depth $MLD(x,y,t)$ gives

$$\int_{-MLD}^\eta \frac{\partial (\rho_0 C_p \Theta \Delta z)}{\partial t} = \int_{-MLD}^\eta \sum_i P_i$$

Using a Leibniz rule for the LHS gives

$$\frac{\partial}{\partial t} \int_{-MLD}^\eta (\rho_0 C_p \Theta \Delta z) - \frac{\partial MLD}{\partial t}\rho_0 C_p \Theta_{ent} = \int_{-MLD}^\eta \sum_i P_i$$

Where $\Theta_{ent}=\Theta(x,y,z=MLD,t)$ is the temperature at the base of the mixed layer. Setting $\int_{-MLD}^\eta (\rho_0 C_p \Theta \Delta z) = \rho_0 C_p \Theta_{MLD} MLD$, where $\Theta_{MLD}$ is the mixed layer average temperature. We thus have:
\begin{align*}
    \frac{\partial (\rho_0 C_p \Theta_{MLD} MLD)}{\partial t} - \frac{\partial MLD}{\partial t}\rho_0 C_p \Theta_{ent} &= \int_{-MLD}^\eta \sum_i P_i \\
    \Longrightarrow \frac{\partial \Theta_{MLD}}{\partial t} + \frac{1}{MLD}\frac{\partial MLD}{\partial t}\left(\Theta_{MLD} - \Theta_{ent}\right) &= \frac{1}{\rho_0 C_p MLD}\int_{-MLD}^\eta \sum_i P_i
\end{align*}

This forms a budget for the tendency of the temperature averaged over the mixed layer (effectively, the SST), where the first term on the LHS is the mixed layer temperature tendency, the second term is the entrainment term and the RHS terms are as before. 

This calculation shows that the entrainment term is not an explicit diagnostic in ACCESS-OM2. However, the above equation suggests a method to compute it. I.e. one could compute a closed budget by computing the mixed layer temperature tendency offline (for full accuracy this should be done with *snapshots* of the temperature rather than time averages) and then computing the entrainment term as a residual from the integral of temp\_tendency over the mixed layer (the LHS of the above equation, divided by MLD). I.e.

$$\frac{1}{MLD}\frac{\partial MLD}{\partial t}\left(\Theta_{MLD} - \Theta_{ent}\right) =  - \frac{\partial \Theta_{MLD}}{\partial t} + \frac{1}{\rho_0 C_p MLD} \int_{-MLD}^\eta temp\_tendency$$


Of course, while it is a closed budget, it's not exactly a budget of the mixed layer temperature because of the averaging time-scale of the diagnostics (e.g. with daily average diagnostics, the terms don't account for subdaily correlations). But it shouldn't be far off. The computations below test this assumption by comparing daily and monthly averaged diagnostics (although the saving of daily averaged diagnostics over a long simulation is rather impractical).

I believe that it is easier to work with the mixed layer temperature budget (as written above), rather than a mixed layer heat content budget, because it is easier to avoid errors associated with mismatches between budget terms and MLD/grid-cell thicknesses. The mixed layer temperature varies much more smoothly with time than the mixed layer heat content (i.e. as the mixed layer depth varies).