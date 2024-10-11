with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  buildInputs = [
    gdal
  ];
  shellHook =
  ''
    source raster_operations.sh
  '';
}
