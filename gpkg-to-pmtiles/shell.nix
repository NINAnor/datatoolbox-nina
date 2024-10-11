with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  buildInputs = [
    pythonPackages.python
    pythonPackages.fiona
    pythonPackages.click
    pythonPackages.django-environ
    gdal
    tippecanoe
  ];
  shellHook = ''
    alias gpkg-to-pmtiles="python main.py"
  '';
}
