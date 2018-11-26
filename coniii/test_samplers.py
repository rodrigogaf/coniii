# =============================================================================================== #
# Testing for samplers.py module.
# Released with ConIII package.
# Author : Eddie Lee, edlee@alumni.princeton.edu
#
# MIT License
# 
# Copyright (c) 2017 Edward D. Lee, Bryan C. Daniels
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================================== #
from .samplers import FastMCIsing,Metropolis
from .utils import define_ising_helper_functions
import numpy as np
import time


def test_Metropolis():
    # Check that everything compiles and runs.
    n=5
    theta=np.random.normal(size=15, scale=.1)
    calc_e, _, _ = define_ising_helper_functions()
    print("Running timing suite for Metropolis sampling functions for n=%d..."%n)

    sampler=Metropolis(n, theta, calc_e, n_cpus=1)
    print("Running sampler.generate_samples(n)")
    sampler.generate_samples(n)
    print("Done.")

    print("Running sampler.generate_samples(n, systematic_iter=True)")
    sampler.generate_samples(n, systematic_iter=True)
    print("Done.")

    print("Running sampler.generate_samples(n, saveHistory=True)")
    sampler.generate_samples(n, saveHistory=True)
    print("Done.")

    print("Running sampler.generate_samples(n, saveHistory=True, systematic_iter=True)")
    sampler.generate_samples(n, saveHistory=True, systematic_iter=True)
    print("Done.")

     # test control over rng
    sampler.rng = np.random.RandomState(0)
    initialSample = np.random.choice([-1.,1], size=(1,n))
    sampler.generate_samples(n, systematic_iter=True, initial_sample=initialSample)
    X1 = sampler.samples.copy()

    sampler.rng = np.random.RandomState(0)
    sampler.generate_samples(n, systematic_iter=True, initial_sample=initialSample)
    X2 = sampler.samples.copy()

    assert np.array_equal(X1, X2), (X1, X2)
   
    # parallelization
    sampler=Metropolis(n, theta, calc_e)
    print("Running sampler.generate_samples(n, saveHistory=True, systematic_iter=True)")
    sampler.generate_samples_parallel(n, systematic_iter=True)
    print("Done.")

    print("Running sampler.generate_samples_parallel(n, systematic_iter=True)")
    sampler.generate_samples_parallel(n, systematic_iter=False)
    print("Done.")

def test_FastMCIsing(run_timing=False):
    # Check that everything compiles and runs.
    n=5
    print("Running timing suite for Ising sampling functions for n=%d..."%n)

    theta=np.random.normal(size=15)
    sampler=FastMCIsing(n, theta)
    print("Running sampler.generate_samples(n)")
    sampler.generate_samples(n)
    print("Done.")

    print("Running sampler.generate_samples(n, systematic_iter=True)")
    sampler.generate_samples(n, systematic_iter=True)
    print("Done.")

    print("Running sampler.generate_samples(n, saveHistory=True)")
    sampler.generate_samples(n, saveHistory=True)
    print("Done.")

    print("Running sampler.generate_samples(n, saveHistory=True, systematic_iter=True)")
    sampler.generate_samples(n, saveHistory=True, systematic_iter=True)
    print("Done.")

    print("Running sampler.generate_samples(n, saveHistory=True, systematic_iter=True)")
    sampler.generate_samples_parallel(n, systematic_iter=True)
    print("Done.")

    print("Running sampler.generate_samples_parallel(n, systematic_iter=True)")
    sampler.generate_samples_parallel(n, systematic_iter=False)
    print("Done.")
    print()

    # test that setting rng reproduces same sample
    sampler=FastMCIsing(n, theta, use_numba=False)
    sampler.rng = np.random.RandomState(0)
    sampler.generate_samples(5, n_iters=20, systematic_iter=True)
    X1 = sampler.samples.copy()
    sampler.rng = np.random.RandomState(0)
    sampler.generate_samples(5, n_iters=20, systematic_iter=True)
    X2 = sampler.samples.copy()
    assert np.array_equal(X1, X2)

    sampler.rng = np.random.RandomState(0)
    sampler.generate_samples_parallel(5, n_iters=20, systematic_iter=True)
    X1 = sampler.samples.copy()
    sampler.rng = np.random.RandomState(0)
    sampler.generate_samples_parallel(5, n_iters=20, systematic_iter=True)
    X2 = sampler.samples.copy()
    assert np.array_equal(X1, X2)

    if run_timing:
        # Some basic timing checks
        print("Timing jit loop")
        t0=time.time()
        sampler.generate_samples(10, n_iters=10000, systematic_iter=True)
        print(time.time()-t0)

        print("Timing parallel jit loop")
        t0=time.time()
        sampler.generate_samples_parallel(10, n_iters=10000, systematic_iter=True)
        print(time.time()-t0)

        print("Timing pure Python loop")
        sampler=FastMCIsing(n, theta, use_numba=False)
        t0=time.time()
        sampler.generate_samples(10, n_iters=10000, systematic_iter=True)
        print(time.time()-t0)

        print("Timing parallel pure Python loop")
        t0=time.time()
        sampler.generate_samples_parallel(10, n_iters=10000, systematic_iter=True)
        print(time.time()-t0)

if __name__=='__main__':
    test_FastMCIsing(True)
