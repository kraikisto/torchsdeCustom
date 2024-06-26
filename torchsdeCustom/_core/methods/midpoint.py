# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from numpy import array
from .. import base_solver
from ...settings import SDE_TYPES, NOISE_TYPES, LEVY_AREA_APPROXIMATIONS


class Midpoint(base_solver.BaseSDESolver):
    weak_order = 1.0
    sde_type = SDE_TYPES.stratonovich
    noise_types = NOISE_TYPES.all()
    levy_area_approximations = LEVY_AREA_APPROXIMATIONS.all()

    def __init__(self, sde, **kwargs):
        self.strong_order = 0.5 if sde.noise_type == NOISE_TYPES.general else 1.0
        super(Midpoint, self).__init__(sde=sde, **kwargs)
        

    

    def step(self, t0, t1, y0):

        dt = t1 - t0
        I_k = self.bm(t0, t1)
        J_k = self.bm2(t0, t1)
        K_k = self.bm3(t0, t1)
        L_k = self.bm4(t0, t1)

        f, g_prod_real = self.sde.f_and_g_prod(t0, y0, I_k)
        g_prod_complex = self.sde.g_prod(t0, y0, K_k)
        h_prod = self.sde.h_prod(t0, y0, J_k)
        p_prod = self.sde.p_prod(t0, y0, L_k)
        half_dt = 0.5 * dt
        
        t_prime = t0 + half_dt
        y_prime = y0 + half_dt * f + 0.5 * (g_prod_real + 1j*g_prod_complex) + 0.5 * h_prod + 0.5 * p_prod

        f_prime, g_prod_real_prime = self.sde.f_and_g_prod(t_prime, y_prime, I_k)
        g_prod_complex_prime = self.sde.g_prod(t_prime, y_prime, K_k)
        h_prod_prime = self.sde.h_prod(t_prime, y_prime, J_k)
        p_prod_prime = self.sde.p_prod(t_prime, y_prime, L_k)
        
        y1 = y0 + dt * f_prime + (g_prod_real_prime + 1j*g_prod_complex_prime) + h_prod_prime + p_prod_prime

        return y1
