with import <nixpkgs> { 
};

let
in pkgs.mkShell rec {
  LD_LIBRARY_PATH = "${stdenv.cc.cc.lib}/lib";
  buildInputs = [
    parallel
    duckdb
    mdbtools
  ];
}