with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  buildInputs = [
    pythonPackages.python
    pythonPackages.duckdb
    pythonPackages.click
  ];
  shellHook = ''
    alias csv-diff="python main.py"
  '';
}
