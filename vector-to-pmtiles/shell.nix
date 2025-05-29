with import <nixpkgs> { };

let
in pkgs.mkShell rec {
  buildInputs = [
    gdal
    tippecanoe
    jq
    parallel
  ];
  LOCALE_ARCHIVE = "${pkgs.glibcLocales}/lib/locale/locale-archive";
  shellHook = ''
    alias vector-to-pmtiles="./vector-to-pmtiles.sh"
  '';
}
