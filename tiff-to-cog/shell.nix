with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  buildInputs = [
    gdal
  ];
  shellHook =
  ''
    source generate_cog.sh
  '';
}
