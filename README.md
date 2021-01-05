# Bow and arrow models by B.W. Kooi

This project aims to provide an implementation of the mathematical models of bow and arrow mechanics developed by B.W. Kooi as described in the following publications:

* Kooi, B.W. & Sparenberg, J.A. 1980 On the static deformation of a bow. Journal of Engineering Mathematics, 14(1):27-45.
* Kooi B.W. 1981 On the mechanics of the bow and arrow. Journal of Engineering Mathematics, 15:119-145.
* Kooi B.W. 1983 On the Mechanics of the Bow and Arrow. PhD thesis, Rijksuniversiteit Groningen.
* Kooi, B.W. 1991. On the mechanics of the modern working-recurve bow. Computational Mechanics, 8: 291-304.
* Kooi, B.W. & Sparenberg, J.A. 1997. On the Mechanics of the Arrow: Archer's Paradox. Journal of Engineering Mathematics, 31(4):285-306.

The complete list of archery publications by B.W. Kooi as well as their manuscripts in pdf form can be found at https://www.bio.vu.nl/thb/users/kooi/.
According to Dr. Kooi, the original programs were written in Algol and Pascal but their source code is no longer available.

# Current state

- [x] Statics of non-recurve bows
- [ ] Statics of recurve bows
- [ ] Dynamics of non-recurve bows
- [ ] Dynamics of recurve bows
- [ ] Dynamics of the arrow

# How to use

This code is written in Python and uses the `numpy` and `scipy` scientific libraries.
The example additionally requires `matplotlib` for visualizing the results.
Install the required dependencies with

```
pip install numpy scipy matplotlib
```

An annotated example for using the bow model can be found under `source/example.py`.
You can run it with

```
python example.py
```

The bow model itself is contained in the file `bow_model.py`.

# Contributing

Contributions that add missing implementations or improve the existing ones are very much welcome.
Note that the goal of this project is not to develop the models any further than what is described in the original papers.
Any such derivative work should be done in a separate repository, but feel free to add a link to this README.

# License

All files in this repository are released under the MIT license.