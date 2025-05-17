using Pkg

dependencies= [
    # networkx
    "osmnx"
    # gtfslib
    # geopandas
    # pandas
    # matplotlib
    # numpy
    # scikit-learn
    # folium
]

Pkg.add(dependencies)

Pkg.add(PackageSpec(url="https://github.com/sisl/Vec.jl.git"))