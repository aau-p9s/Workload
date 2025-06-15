{
    inputs = {
        nixpkgs.url = "nixpkgs/nixos-25.05";
    };
    outputs = { self, nixpkgs }: let
        system = "x86_64-linux";
        pkgs = import nixpkgs { inherit system; };
    in {
        devShells.${system}.default = pkgs.mkShellNoCC {
            packages = with pkgs; [
                (python3.withPackages (py: with py; [
                    numpy
                    ipython
                    locust
                    matplotlib
                ]))
            ];
        };
    };
}
