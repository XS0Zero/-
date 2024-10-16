from matlab_project.BWRSV1 import BWRSV1_func
def JL4(P1, T1, Qg, r, k, R, Pc, Tc, Pci, Tci, Pflq):
    T1 += 273.15  # Convert Celsius to Kelvin
    Pr1 = P1 / Pc  # Pressure before throttling
    Tr1 = T1 / Tc  # Temperature before throttling

    Z1 = BWRSV1_func(P1, T1)  # Call to the BWRSV1 function
    P2 = Pflq

    a0 = (P2 / P1) ** (2 / k) - (P2 / P1) ** ((k + 1) / k)
    b0 = k / (k - 1)

    d1 = (((Qg / 10000) * (r * T1 * Z1) ** 0.5) / (0.4066 * P1 * (a0 * b0) ** 0.5)) ** 0.5

    # Cp calculation
    Cp = (13.19 + 0.09224 * (273 + T1 - 14) -
          ((273 + T1 - 14) ** 2) * 0.00006238 +
          (0.9965 * 29.16 * r * ((P1 + P2) * 5) ** 1.124 /
           (((273 + T1 - 17) / 100) ** 5.08)))

    w = 0.013  # Methane eccentric factor
    m = 0.48 + 1.574 * w - 0.176 * w ** 2
    beta = (1 + m * (1 - Tr1 ** 0.5)) ** 2
    ra = 0.42747 * beta * Tci ** 2 / Pci
    rb = 0.08664 * Cp * Tci / Pci
    A = ra * P1 / T1
    B = rb * P1 / T1
    f = (2.343 * ((T1 - 14) / Tci) ** (-2.04) -
         0.071 * ((P1 + P2) / (2 * Pci) - 0.8))

    Cj = Tci * f * 4.1868 / (Pci * Cp)

    DertaT = Cj * (P1 - P2)
    T2 = T1 - DertaT - 273.15  # Throttling temperature in Celsius

    d = d1
    Qg1 = Qg

    return P2, T2, d, Qg1