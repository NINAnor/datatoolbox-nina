let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
  pkgs = import nixpkgs { config = { }; overlays = []; };
  system_packages = builtins.attrValues {
    inherit (pkgs) 
      uv
      git
      cacert
    ;
  };
  pypkgs = builtins.attrValues {
    inherit (pkgs.python312Packages)
      # https://github.com/Breakthrough/DVR-Scan/blob/v1.7-dev1/requirements.txt
      tkinter
      numpy
      opencv4
      #opencv-contrib-python
      pillow
      platformdirs
      pytest
      #scenedetect>=0.6.2
      screeninfo
      tqdm
    ;
  };
in
pkgs.mkShellNoCC {
  buildInputs = [ pypkgs system_packages ];
  shellHook = ''
    export PATH="$PATH:$PWD"
  '';
}
